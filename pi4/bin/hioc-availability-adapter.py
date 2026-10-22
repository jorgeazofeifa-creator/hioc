#!/usr/bin/env python3
"""Explicit private PE-7 adapter entry. No listener, key creation or migration by default."""
import argparse
from pathlib import Path
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description='Disabled-by-default private HIOC operator adapter')
    parser.add_argument('--home', type=Path, required=True)
    parser.add_argument('--configuration', type=Path, required=True)
    parser.add_argument('--serve', action='store_true')
    args = parser.parse_args(argv)
    if not args.serve:
        print('PE7_ADAPTER=DISABLED'); return 0
    sys.path.insert(0, str(args.home/'pi4/lib'))
    from hioc.asset_policy import PolicyStore, PolicyService
    from hioc.availability_contract import keys, require, strict_json
    from hioc.availability_protocol import IssuerTrust, Protocol, ObservationTrust, ObservationProtocol
    from hioc.availability_observation import ObservationStore
    from hioc.availability import validate_profile
    from hioc.availability_server import create_server, private_file, server_context
    from hioc.availability import AvailabilityReader
    from hioc.availability_incidents import EngineState
    from datetime import datetime, timezone
    try:
        def configuration():
            raw = Path(private_file(args.configuration)).read_bytes()
            value = strict_json(raw, limit=262144, depth=8)
            required = {'enabled','bind_address','port','ha_address','server_certificate','server_key','client_ca','issuer_trusts'}
            require(set(value) in (required, required | {'observation_trusts','profile_file'}))
            require(value['enabled'] is True)
            return value
        settings = configuration()
        def trust_lookup(issuer, key_id):
            # Re-read ACL/revocation and key material on every request and writer recheck.
            matches = [entry for entry in configuration()['issuer_trusts']
                       if entry.get('issuer') == issuer and entry.get('key_id') == key_id]
            require(len(matches) == 1, 'TRUST_INVALID')
            entry = matches[0]
            keys(entry, ('issuer', 'key_id', 'assertion_key_file', 'client_spki_sha256', 'actors', 'enabled'))
            key = Path(private_file(entry['assertion_key_file'], secret=True)).read_bytes()
            actors = {actor:{operation:frozenset(allowed) for operation,allowed in operations.items()}
                      for actor,operations in entry['actors'].items()}
            return IssuerTrust(issuer, key_id, key, entry['client_spki_sha256'], actors, entry['enabled'])
        store = PolicyStore(args.home)
        service = PolicyService(store)
        observation_protocol = None
        if 'observation_trusts' in settings:
            def profiles(asset_id):
                value = strict_json(Path(private_file(configuration()['profile_file'])).read_bytes(), limit=262144, depth=8)
                return validate_profile(value[asset_id])
            def observation_trust(issuer,key_id):
                entries = [x for x in configuration()['observation_trusts'] if x.get('issuer')==issuer and x.get('key_id')==key_id]
                require(len(entries)==1,'TRUST_INVALID')
                entry=entries[0]
                keys(entry,('issuer','key_id','assertion_key_file','client_spki_sha256','sources','enabled'))
                key=Path(private_file(entry['assertion_key_file'],secret=True)).read_bytes()
                for operator in configuration()['issuer_trusts']:
                    require(operator['client_spki_sha256'] != entry['client_spki_sha256'], 'TRUST_INVALID')
                    require(Path(private_file(operator['assertion_key_file'],secret=True)).read_bytes() != key, 'TRUST_INVALID')
                return ObservationTrust(issuer,key_id,key,entry['client_spki_sha256'],
                    {k:frozenset(v) for k,v in entry['sources'].items()},entry['enabled'])
            observation_protocol=ObservationProtocol(ObservationStore(args.home,Path('/tmp/hioc-pe7-observations.lock')),
                observation_trust,profiles,service.attachment)
        context = server_context(settings['server_certificate'], settings['server_key'], settings['client_ca'])
        reader = AvailabilityReader(service, EngineState(args.home/'state/incidents/pe7.json', Path('/tmp/hioc-incident-engine.lock')),
            lambda: datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        server = create_server(settings['bind_address'], settings['port'], context, Protocol(service, trust_lookup, status_reader=reader),
                               enabled=settings['enabled'], allowed_ha_address=settings['ha_address'], observation_protocol=observation_protocol)
        try: server.serve_forever()
        finally: server.server_close()
        return 0
    except Exception:
        print('PE7_ADAPTER=FAIL_CLOSED', file=sys.stderr); return 1


if __name__ == '__main__':
    raise SystemExit(main())
