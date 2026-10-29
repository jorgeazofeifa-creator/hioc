# PE-7.3 Owner-Directed Full-Inventory Asset Authorization Amendment

Status: ACCEPTED — OWNER-DIRECTED SUCCESSOR AUTHORIZATION.
Identifier: PE73_FULL_INVENTORY_ASSET_AUTHORIZATION_V1.
Owner acceptance: HIOC PE-7.3: Finalize and Publish the Qualified Release Candidate.
This explicit owner direction adopts the population grants below, including
availability_status=existing_assets as a deliberate successor change to section 6.1.
Publication does not authorize production provisioning, migration or activation.
The original PE-7 contract remains unchanged and historically authoritative.

## Original requirement and demonstrated gap

The accepted implementation contract section 5 requires independent issuer,
HA administrator actor, operation and independent Asset scope; the accepted
implementation used exact Asset-ID grants. Section 6.1 explicitly requires an
exact-Asset-ID availability-status read grant. This accepted successor amendment
deliberately permits population-level availability_status=existing_assets for each
explicitly granted actor, while preserving its independent operation boundary.
Exact IDs remain supported.
Operator-supplied PI3 evidence reports 203 discovered devices, a readable authoritative
Asset store at schema1.0 with zero records and online Asset status. This is not a
fixed inventory size or a machine-observed Codex production fact. Requiring an
existing Asset list for enrollment prevents zero-Asset bootstrap and makes future
growth require repeated ACL reconstruction. Discovery alone never creates Assets.

## Precise extension

Each explicitly selected actor and operation may retain its exact-ID set/list OR
use one closed grant object with exactly these fields:

- scope: the operation-specific value in the table below;
- amendment: PE73_FULL_INVENTORY_ASSET_AUTHORIZATION_V1;
- acceptance_reference: the separately recorded owner acceptance reference.

| Operation | Permitted scope | Authoritative population |
| --- | --- | --- |
| get | eligible_or_existing | Existing schema2.0 Asset OR currently eligible discovered device, to read revisions before explicit creation. |
| create | eligible_inventory | One requested strongly and unambiguously MAC-derived device in a fresh validated authoritative inventory. |
| update | existing_assets | One already existing Asset; original revision, field and ON-eligibility checks remain. |
| result | existing_assets | One existing Asset and receipt belonging to the same issuer/actor/operation ID. |
| availability_status | existing_assets | One existing Asset, separate audience, route, read grant and quotas. |

No '*' token, arbitrary operation, broad identifier pattern, request-supplied scope,
privileged browser identity or implicit cross-operation authority is supported.
The packet can hold an unapproved grant with a null acceptance_reference only while
inactive. An enabled issuer with any unaccepted population grant fails closed.
An acceptance reference in a local config is not itself evidence of owner approval:
production provisioning must bind it to the actual separately accepted amendment.
The owner acceptance above supplies the amendment authority, not an operator ID
or production ACL. Production configuration must bind its acceptance_reference to
this accepted owner decision; no actor or operation is implicitly granted.

## Independent backend conditions

All existing mTLS/SPKI, exact32-byte HMAC, signature/payload/path/audience, fresh
<=30-second actor assertions, replay nonce, rate and receipt limits remain.
HA independently checks a directly authenticated active non-system administrator,
normal unexpired provider-validated refresh token, live WebSocket context and
explicit HA operator allowlist. Human identity never comes from browser data.
The backend rereads its own persisted issuer/actor/operation grant and key material
for each request and writer-guard reauthorization. Removing/disabling the grant,
actor, issuer or key denies subsequent requests; HA token limitations remain as in
the original contract. Scope authority is independent of HA's administrator flag.

Creation uses the accepted inventory validator/freshness bound and strong-owner
resolver: unique normalized MAC ownership, exact stable-device-ID recomputation,
no duplicated owner/ID conflict, no future/stale input, no orphan/weak identity.
Neither 203 nor an enrollment-time snapshot becomes an ACL. Newly discovered
eligible devices qualify only at request time; one deliberate operation creates
one Asset. Existing create conflicts cannot overwrite a record. Exact retained
create receipts can still reconcile the same logical operation; this does not
authorize a new creation or update to an existing record.

Membership and grant checks repeat under the existing exclusive Asset writer guard,
without nested locks. Epoch/store/record revision checks, durable backups/status,
120-second idempotency receipts, provenance operator_ha and field validation remain.
Existing Asset management does not require the device to remain discoverable, so
safe OFF/metadata policy edits and reads can manage orphans. Turning availability
ON still requires current strong attachment. No identity, canonical-IP, health,
incident, notification, deletion or arbitrary metadata-writing authority is added.

## Operator grants, revocation and persistence

Provisioning offers explicit exact/population mode. Population mode asks for the
actual approved HA actor and selected operations, with separate status-read choice;
it never asks for a hand-maintained Asset-ID list. No actor, private port, subject,
acceptance reference or production credential is invented. Grants persist in the
existing protected backend configuration and are read again after restart, not
expanded into a cached device/Asset list. Exact-ID grants retain their prior rules.
Revocation does not require CA renewal or Asset deletion; it changes backend grant
authority. CA/passphrase, runtime HMAC/server key and PI5 client-key custody stay
separate under the accepted trust architecture.

The already validated PI3/PI5 dependency environments and root custody preparation
remain accepted OPERATOR_SUPPLIED evidence. Their sealed historical toolkits are
not rewritten. The new repository source is not installed by this publication.
Before production use, guarded source/toolkit delivery must
qualify the successor implementation against those existing seals. A legacy sealed
helper rejecting the extended plan is a safe refusal, not permission to bypass its
pin or silently replace its files. No CA key or certificate is created here.

## Migration, Dashboard and rollout boundaries

The authoritative schema1.0 store, including zero records, remains valid. Requests
do not initialize or migrate it; schema2.0 requires its separately authorized exact
1.0-to-2.0 migration under stopped writers. No migration is performed by this work.
Exclusive UI remains hioc-dashboard-v2, inventory view hioc-v2-inventory. The existing
dynamic inventory selector and explicit save/create flow remain byte-identical. Six views,
navigation, existing layout and unrelated content are preserved. No discovery-driven
creation, editing activation, evaluator, recurring job or notification is enabled.

## Acceptance requirements

Repository tests must cover zero-store explicit first/subsequent creation, inventory
growth/shrinkage, fresh identity rederivation, weak/conflicted/stale/orphan rejection,
forged IDs, non-admin/missing/revoked operators, independent per-operation grants,
status/result separation, privilege escalation, replay, quotas, epoch/revisions,
writer-time drift/revocation and restart-persisted grants. Existing exact-ID rules,
full native suite, privacy/cross-phase bindings and protected449 identities must pass.
Original contract text, immutable13 PI3/six HA payloads, historical production receipts
and executive authorization decision remain unchanged. Current successor identity
bindings may be refreshed only for actually changed authorized implementation paths.

PE-7.3 remains IN_PROGRESS. PE-7.4 remains NOT_AUTHORIZED.
Next milestone: separately guarded successor artifact/toolkit delivery into the
existing HIOC Dashboard v2 architecture. No runtime delivery is performed here.
