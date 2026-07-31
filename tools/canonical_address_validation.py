#!/usr/bin/env python3
"""Evaluate the bounded ADR-0018 production-validation case from captured evidence."""

import argparse
import ipaddress
import json
import time
from pathlib import Path


HIGHER_RANKED_SOURCES = {"local_host", "gateway"}
HIGHER_RANKED_NEIGHBOR_STATES = {"REACHABLE", "PERMANENT"}


def canonical_ipv4(value):
    try:
        address = ipaddress.ip_address(str(value or "").strip())
    except ValueError:
        return None
    if not isinstance(address, ipaddress.IPv4Address):
        return None
    if (
        address.is_unspecified
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address == ipaddress.IPv4Address("255.255.255.255")
    ):
        return None
    return str(address)


def normalized_mac(value):
    return str(value or "").strip().lower().replace("-", ":")


def record_sources(record):
    sources = record.get("sources", [])
    if isinstance(sources, str):
        sources = [item.strip() for item in sources.split(",") if item.strip()]
    source = str(record.get("source", "")).strip()
    if source:
        sources = list(sources) + [item.strip() for item in source.split(",") if item.strip()]
    return set(sources)


def active_leases(leases, now_epoch):
    result = {}
    for lease in leases:
        ip = canonical_ipv4(lease.get("ip"))
        mac = normalized_mac(lease.get("mac"))
        try:
            expiry = int(lease.get("expiry", lease.get("lease_expires_epoch", 0)) or 0)
        except (TypeError, ValueError):
            continue
        if mac and ip and (expiry == 0 or expiry > now_epoch):
            result.setdefault(mac, []).append({**lease, "ip": ip, "mac": mac, "expiry": expiry})
    return result


def find_qualifying_candidates(inventory, leases, neighbors, now_epoch=None, historical_inventory=None):
    now_epoch = int(time.time()) if now_epoch is None else int(now_epoch)
    devices = inventory.get("devices", [])
    historical_by_mac = {
        normalized_mac(item.get("mac")): item
        for item in (historical_inventory or {}).get("devices", [])
        if normalized_mac(item.get("mac"))
    }
    devices_by_mac = {}
    for device in devices:
        mac = normalized_mac(device.get("mac"))
        if mac:
            devices_by_mac.setdefault(mac, []).append(device)
    leases_by_mac = active_leases(leases, now_epoch)
    neighbors_by_mac = {}
    for neighbor in neighbors:
        mac = normalized_mac(neighbor.get("mac"))
        ip = canonical_ipv4(neighbor.get("ip"))
        state = str(neighbor.get("state", "")).strip().upper()
        if mac and ip:
            neighbors_by_mac.setdefault(mac, []).append({**neighbor, "mac": mac, "ip": ip, "state": state})

    candidates = []
    exclusions = []
    for mac, mac_leases in sorted(leases_by_mac.items()):
        identities = devices_by_mac.get(mac, [])
        stale = [
            item for item in neighbors_by_mac.get(mac, [])
            if item["state"] == "STALE"
            and all(item["ip"] != lease["ip"] for lease in mac_leases)
        ]
        if not stale:
            continue
        reasons = []
        if len(identities) != 1:
            reasons.append(f"identity_count={len(identities)}")
        device = identities[0] if len(identities) == 1 else {}
        sources = record_sources(device)
        if sources & HIGHER_RANKED_SOURCES or any(source.startswith("integration:") for source in sources):
            reasons.append("higher_ranked_source")
        if any(
            item["state"] in HIGHER_RANKED_NEIGHBOR_STATES
            for item in neighbors_by_mac.get(mac, [])
        ):
            reasons.append("higher_ranked_neighbor")
        historical = historical_by_mac.get(mac)
        if historical:
            historical_ip = canonical_ipv4(historical.get("ip"))
            if historical_ip not in {item["ip"] for item in stale}:
                reasons.append("historical_canonical_not_stale_candidate")
        item = {
            "mac": mac,
            "active_dhcp_ipv4": sorted({lease["ip"] for lease in mac_leases}),
            "stale_neighbor_ipv4": sorted({neighbor["ip"] for neighbor in stale}),
            "canonical_ipv4": canonical_ipv4(device.get("ip")),
            "device_id": device.get("id"),
            "sources": sorted(sources),
            "historical_canonical_ipv4": canonical_ipv4(historical.get("ip")) if historical else None,
        }
        if reasons:
            exclusions.append({**item, "exclusion_reasons": reasons})
        else:
            candidates.append(item)
    return candidates, exclusions


def evaluate(inventory, leases, neighbors, invariants=None, now_epoch=None, historical_inventory=None):
    candidates, exclusions = find_qualifying_candidates(
        inventory,
        leases,
        neighbors,
        now_epoch=now_epoch,
        historical_inventory=historical_inventory,
    )
    failed_invariants = sorted(name for name, value in (invariants or {}).items() if not value)
    if failed_invariants:
        result = "FAIL"
    elif not candidates:
        result = "NO_QUALIFYING_CANDIDATE"
    elif all(candidate["canonical_ipv4"] in candidate["active_dhcp_ipv4"] for candidate in candidates):
        result = "PASS"
    else:
        result = "FAIL"
    return {
        "result": result,
        "qualifying_candidates": candidates,
        "excluded_candidates": exclusions,
        "failed_invariants": failed_invariants,
        "rollback_recommended": result == "FAIL",
    }


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--leases", required=True)
    parser.add_argument("--neighbors", required=True)
    parser.add_argument("--invariants")
    parser.add_argument("--historical-inventory")
    parser.add_argument("--now-epoch", type=int)
    args = parser.parse_args()
    report = evaluate(
        load_json(args.inventory),
        load_json(args.leases),
        load_json(args.neighbors),
        load_json(args.invariants) if args.invariants else None,
        args.now_epoch,
        load_json(args.historical_inventory) if args.historical_inventory else None,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["result"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
