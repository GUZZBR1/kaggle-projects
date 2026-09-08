import hashlib
import json

from arena.agents import ROOT, load_agent


def test_public_opponent_registry_matches_the_pinned_artifacts():
    manifest = json.loads((ROOT / 'opponents' / 'manifest.json').read_text())
    entries = {entry['id']: entry for entry in manifest}
    expected = {
        'cok_v10': 'opponents/public/cok_v10/main.py',
        'seyamalam_v21': 'opponents/public/seyamalam_v21/main.py',
        'lonespear_v11': 'opponents/public/lonespear_v11/main.py',
    }
    for opponent_id, path in expected.items():
        entry = entries[opponent_id]
        source = ROOT / path
        assert entry['path'] == path
        assert entry['source_url'].startswith('https://github.com/')
        assert entry['captured_at'] == '2026-09-07'
        assert entry['engine']['kaggle_environments'] == '1.32.7'
        assert entry['engine']['interpreter_sha256'] == (
            'bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e'
        )
        assert hashlib.sha256(source.read_bytes()).hexdigest() == entry['sha256']
        assert callable(load_agent(path))
        main_manifest = json.loads(source.with_suffix('.manifest.json').read_text())
        assert main_manifest['id'] == opponent_id
        assert main_manifest['sha256'] == entry['sha256']
        assert main_manifest['commit'] == entry['commit']
        assert main_manifest['license'] == entry['license']
