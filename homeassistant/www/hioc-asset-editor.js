/* Local HA card: drafts are never authority. No browser-to-adapter connection. */
const HIOC_TYPES = [
  ["router_gateway", "Router / Gateway"], ["raspberry_pi_server", "Raspberry Pi / Server"],
  ["network_switch", "Network Switch"], ["wireless_access_point_mesh_node", "Wireless Access Point / Mesh Node"],
  ["smart_home_hub_bridge", "Smart Home Hub / Bridge"], ["other_infrastructure", "Other Infrastructure"],
];
const HIOC_PENDING = new Set();
class HiocAssetEditor extends HTMLElement {
  setConfig(config) {
    if (!config || (config.asset_id && !/^dev_[0-9a-f]{16}$/.test(config.asset_id)) ||
        (!config.asset_id && config.inventory_entity !== "sensor.hioc_inventory_devices")) throw new Error("An explicit Asset ID or supported inventory selector is required");
    this.config = {...config}; this.confirmed = null; this.draft = null;
    this.status = null; this.statusPhase = "unavailable"; this.statusGeneration = 0;
    this.phase = "loading"; this.generation = 0; this.operation = null; this.render();
  }
  set hass(value) {
    this._hass = value;
    if (this.config && this.config.asset_id && !this.loaded) { this.loaded = true; void this.reload(); }
    else if (this.config && !this.config.asset_id) this.render();
  }
  getCardSize() { return 5; }
  async service(service, data) {
    if (!this._hass || typeof this._hass.callWS !== "function") throw new Error("Service unavailable");
    const result = await this._hass.callWS({type: "call_service", domain: "hioc_operator", service,
      service_data: data, return_response: true});
    const response = result && result.response;
    if (!response || response.schema_version !== "1.0") throw new Error("Service unavailable");
    return response;
  }
  async reload() {
    if (HIOC_PENDING.has(this.config.asset_id)) return;
    const generation = ++this.generation;
    this.phase = "loading"; this.render();
    try {
      const response = await this.service("get_policy", {asset_id: this.config.asset_id});
      if (generation !== this.generation) return;
      if (response.result !== "read" || response.commit_state !== "CONFIRMED") throw new Error("Read unavailable");
      this.accept(response.policy); this.phase = "ready"; await this.readStatus();
    } catch (_) { if (generation === this.generation) this.phase = "unavailable"; }
    this.render();
  }
  accept(policy) {
    if (!policy || policy.asset_id !== this.config.asset_id) throw new Error("Policy unavailable");
    this.confirmed = {...policy};
    this.draft = Object.fromEntries(["expected_availability", "infrastructure_device", "infrastructure_type"]
      .map(key => [key, policy[key]]));
  }
  async save() {
    const key = this.config.asset_id;
    if (this.phase !== "ready" || !this.confirmed || HIOC_PENDING.has(key)) return;
    if (this.confirmed.revision === null && this.confirmed.attachment !== "strong") return;
    if (this.draft.expected_availability === true && this.confirmed.attachment !== "strong") return;
    HIOC_PENDING.add(key); ++this.generation;
    const operation_id = crypto.randomUUID().replaceAll("-", "");
    const data = {asset_id: key, store_epoch: this.confirmed.store_epoch,
      expected_store_revision: this.confirmed.store_revision, expected_revision: this.confirmed.revision,
      operation_id, fields: {...this.draft}};
    this.operation = {operation_id, asset_id: key};
    this.status = null; this.statusPhase = "unavailable"; ++this.statusGeneration;
    this.phase = "saving"; this.render();
    try {
      const response = await this.service(this.confirmed.revision === null ? "create_asset_policy" : "update_asset_policy", data);
      if (response.result === "error") {
        this.phase = response.error_code === "REVISION_CONFLICT" ? "conflict" :
          response.commit_state === "UNKNOWN" ? "uncertain" : "failed";
      } else if (response.commit_state === "CONFIRMED" && response.operation_id === operation_id) {
        this.accept(response.policy); this.phase = "ready"; this.operation = null; await this.readStatus();
      } else this.phase = "uncertain";
    } catch (_) { this.phase = "uncertain"; }
    finally { HIOC_PENDING.delete(key); this.render(); }
  }
  async reconcile() {
    if (!this.operation || HIOC_PENDING.has(this.config.asset_id)) return;
    HIOC_PENDING.add(this.config.asset_id); this.phase = "reconciling"; this.render();
    try {
      const response = await this.service("get_operation_result", {...this.operation});
      if (response.result === "found" && response.commit_state === "CONFIRMED") {
        this.accept(response.policy); this.operation = null; this.phase = "ready"; await this.readStatus();
      } else this.phase = "uncertain";
    } catch (_) { this.phase = "uncertain"; }
    finally { HIOC_PENDING.delete(this.config.asset_id); this.render(); }
  }
  async readStatus() {
    const generation = ++this.statusGeneration;
    const key = this.config.asset_id;
    this.status = null; this.statusPhase = "loading";
    try {
      const response = await this.service("get_availability_status", {asset_id:key});
      if (generation !== this.statusGeneration || key !== this.config.asset_id) return;
      if (!["READ", "NOT_EVALUATED", "UNAVAILABLE"].includes(response.result) || response.asset_id !== key) throw new Error("Status unavailable");
      // Closed response validation is performed at the authenticated HA bridge.
      this.status = response; this.statusPhase = response.result;
    } catch (_) { if (generation === this.statusGeneration) { this.status = null; this.statusPhase = "unavailable"; } }
  }
  element(tag, text) { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; return node; }
  render() {
    this.replaceChildren(); if (!this.config) return;
    const card = this.element("ha-card"); card.setAttribute("header", "HIOC Asset policy");
    const body = this.element("div"); body.style.padding = "16px";
    if (!this.config.asset_id) {
      body.append(this.element("p", "Select a discovered device to read its policy. Viewing creates no Asset."));
      const devices = this._hass?.states?.[this.config.inventory_entity]?.attributes?.devices;
      const select = this.element("select"); select.setAttribute("aria-label", "Asset device");
      const placeholder = this.element("option", "Select device"); placeholder.value = ""; select.append(placeholder);
      if (Array.isArray(devices) && devices.length <= 4096) {
        const seen = new Set();
        for (const device of devices) if (/^dev_[0-9a-f]{16}$/.test(device.id || "") && !seen.has(device.id)) {
          seen.add(device.id); const option = this.element("option", `${device.display_name || device.name || "Device"} (${device.id})`);
          option.value = device.id; select.append(option);
        }
      } else select.disabled = true;
      select.addEventListener("change", () => { if (select.value) { this.config.asset_id = select.value; this.loaded = true; void this.reload(); } });
      body.append(select); card.append(body); this.append(card); return;
    }
    body.append(this.element("p", this.config.asset_id));
    const messages = {loading: "Loading saved policy", unavailable: "Unavailable / unauthorized; no policy assumed",
      ready: "Backend-confirmed policy; unsaved drafts remain separate", saving: "Saving; awaiting backend confirmation",
      conflict: "Revision conflict: reload, then explicitly reapply your edit", failed: "Save failed; confirmed policy retained",
      uncertain: "Save outcome uncertain. Read saved result; do not retry the mutation", reconciling: "Reading saved result"};
    body.append(this.element("p", messages[this.phase] || "Unavailable"));
    const enabled = this.phase === "ready" && this.confirmed;
    if (this.confirmed) {
      body.append(this.element("p", `Attachment: ${this.confirmed.attachment}; persisted revision: ${this.confirmed.revision ?? "no Asset"}`));
      const state = this.status;
      if (!state || state.policy_binding !== "CURRENT" || state.applied_policy_revision !== this.confirmed.revision)
        body.append(this.element("p", "Pending next valid evaluation; persistence is not application"));
      body.append(this.element("p", `Availability status: ${this.statusPhase}`));
      if (state) {
        body.append(this.element("p", `Saved revision: ${this.confirmed.revision ?? "none"}; last applied revision: ${state.applied_policy_revision ?? "not established"}; policy binding: ${state.policy_binding}`));
        if (state.evaluation) {
          const e = state.evaluation;
          const expiry = e.valid_until ? Date.parse(e.valid_until) : NaN;
          const fresh = e.freshness === "FRESH" && Number.isFinite(expiry) && Date.now() < expiry && Date.now() >= Date.parse(e.evaluated_at);
          const samePolicy = state.policy_binding === "CURRENT" && state.current_policy_revision === this.confirmed.revision && state.expected_availability === this.confirmed.expected_availability;
          body.append(this.element("p", `${fresh && samePolicy ? "Evaluated snapshot at read; expires at displayed deadline" : "Last-known evaluation; not current"}: ${e.availability_state}; reason: ${e.reason_code}; scope: ${e.evidence_scope}`));
          body.append(this.element("p", `Evaluated at ${e.evaluated_at}; exclusive deadline ${e.valid_until ?? "unknown"}; read at ${state.read_at}`));
          for (const row of state.observations || []) body.append(this.element("p", `Source ${row.source_ref}: ${row.scope}; ${row.collection_status}; ${row.completeness}; ${row.freshness}`));
        } else body.append(this.element("p", state.result === "NOT_EVALUATED" ? "Not evaluated" : `Status unavailable: ${state.status_reason}`));
      } else body.append(this.element("p", "Status unavailable; no evaluated state assumed"));
      body.append(this.element("p", "Operator-owned policy; edits use authenticated Home Assistant provenance"));
      for (const [key, title] of [["expected_availability", "Expected Availability"], ["infrastructure_device", "Infrastructure Device"]]) {
        const row = this.element("div"); const label = this.element("label", title + " ");
        const toggle = this.element("input"); toggle.type = "checkbox"; toggle.checked = this.draft[key] === true;
        toggle.disabled = !enabled || (key === "expected_availability" && this.confirmed.attachment !== "strong" && this.draft[key] !== true);
        toggle.setAttribute("aria-label", title); toggle.addEventListener("change", () => { this.draft[key] = toggle.checked; this.render(); });
        label.append(toggle); row.append(label, this.element("span", this.draft[key] === null ? " Not configured (effective OFF)" : this.draft[key] ? " ON" : " OFF"));
        const reset = this.element("button", "Reset to unconfigured"); reset.disabled = !enabled;
        reset.addEventListener("click", () => { this.draft[key] = null; this.render(); }); row.append(reset); body.append(row);
      }
      if (this.draft.infrastructure_device === true) {
        const label = this.element("label", "Infrastructure Type "); const select = this.element("select"); select.disabled = !enabled;
        for (const [value, title] of [["", "Unassigned / Unknown"], ...HIOC_TYPES]) {
          const option = this.element("option", title); option.value = value; select.append(option);
        }
        select.value = this.draft.infrastructure_type ?? "";
        select.addEventListener("change", () => { this.draft.infrastructure_type = select.value || null; });
        label.append(select); body.append(label);
      }
      const save = this.element("button", this.confirmed.revision === null ? "Create Asset and Save" : "Save policy");
      save.disabled = !enabled || (this.confirmed.revision === null && this.confirmed.attachment !== "strong");
      save.addEventListener("click", () => { void this.save(); }); body.append(save);
    }
    const reload = this.element("button", "Reload confirmed policy");
    reload.disabled = HIOC_PENDING.has(this.config.asset_id); reload.addEventListener("click", () => { void this.reload(); }); body.append(reload);
    if (this.operation) { const read = this.element("button", "Read saved result"); read.disabled = HIOC_PENDING.has(this.config.asset_id);
      read.addEventListener("click", () => { void this.reconcile(); }); body.append(read); }
    card.append(body); this.append(card);
  }
}
customElements.define("hioc-asset-editor", HiocAssetEditor);
