import copy
import hashlib
import json

import pytest

from experiments.public_base_tournament import analyze_tournament, validate_entry


def entry(tmp_path, **changes):
    artifact = tmp_path / 'agent.py'
    artifact.write_text('def agent(obs, config=None): return {}\n')
    base = {
        'id': 'public-a', 'family': 'family-a', 'path': str(artifact),
        'sha256': hashlib.sha256(artifact.read_bytes()).hexdigest(),
        'license': 'Apache-2.0', 'engine': {'name': 'kaggriculture', 'version': '1.32.7'},
        'lineage': 'independent-a', 'adaptation_notes': 'clock adapter only',
        'repository': 'https://example.test/a', 'commit': 'abc123',
    }
    return {**base, **changes}


def test_provenance_gate_checks_hash_license_engine_and_lineage(tmp_path):
    assert validate_entry(entry(tmp_path))['source'] == 'https://example.test/a'
    for changes in ({'license': 'unknown'}, {'engine': {'version': 'old'}},
                    {'engine': {'version': '1.32.7', 'interpreter_sha256': 'wrong'}},
                    {'lineage': ''}, {'sha256': '0' * 64}):
        with pytest.raises(ValueError):
            validate_entry(entry(tmp_path, **changes))


def row(candidate, opponent, seed, seat, score, money=100):
    return {
        'candidate': candidate, 'opponent': opponent, 'candidate_hash': candidate + '-hash',
        'opponent_hash': opponent + '-hash', 'seed': seed, 'seat': seat, 'score': score,
        'money': money, 'opponent_money': 100, 'margin': money - 100, 'steps': 719,
        'backend': 'fast', 'configuration': {}, 'environment': {}, 'failures': [],
        'opponent_failures': [], 'audit': {}, 'sales': {}, 'telemetry_version': None,
        'daily': None, 'opponent_daily': None, 'runtime_ms': [1], 'unsold_items': 0,
    }


def test_selection_uses_worst_family_not_best_aggregate():
    candidates = [
        {'id': 'v002', 'family': 'internal', 'path': 'v002', 'agent_spec': 'v002', 'sha256': 'a',
         'lineage': 'i', 'source': 'repo', 'version': 'v002'},
        {'id': 'spiky', 'family': 'spiky', 'path': 'spiky', 'agent_spec': 'spiky', 'sha256': 'b',
         'lineage': 's', 'source': 'repo', 'version': '1'},
        {'id': 'robust', 'family': 'robust', 'path': 'robust', 'agent_spec': 'robust', 'sha256': 'c',
         'lineage': 'r', 'source': 'repo', 'version': '1'},
    ]
    opponents = [
        {'id': 'o1', 'family': 'one', 'path': 'o1'},
        {'id': 'o2', 'family': 'two', 'path': 'o2'},
        {'id': 'o3', 'family': 'three', 'path': 'o3'},
    ]
    rates = {'v002': [0, 0, 0], 'spiky': [1, 1, 0], 'robust': [.5, .5, .5]}
    results = {}
    for candidate in candidates:
        rows = []
        for opponent, score in zip(opponents, rates[candidate['id']]):
            rows += [row(candidate['id'], opponent['path'], seed, seat, score)
                     for seed in (1, 2) for seat in (0, 1)]
        results[candidate['id']] = rows
    decision = analyze_tournament(results, candidates, opponents, min_seed_blocks=2)
    assert decision['selected_base']['id'] == 'robust'
    assert decision['metrics']['spiky']['aggregate']['score_rate'] > decision['metrics']['robust']['aggregate']['score_rate']


def test_selection_refuses_insufficient_or_failed_evidence():
    candidates = [{'id': name, 'family': name, 'path': name, 'agent_spec': name, 'sha256': name,
                   'lineage': name, 'source': 'repo', 'version': '1'}
                  for name in ('v002', 'a', 'b')]
    opponents = [{'id': name, 'family': name, 'path': name} for name in ('x', 'y', 'z')]
    results = {candidate['id']: [row(candidate['id'], opponent['path'], 1, seat, .5)
                                 for opponent in opponents for seat in (0, 1)]
               for candidate in candidates}
    with pytest.raises(ValueError, match='fewer than'):
        analyze_tournament(results, candidates, opponents, min_seed_blocks=2)
    results['a'][0]['failures'] = [{'kind': 'boom'}]
    with pytest.raises(ValueError, match='failures'):
        analyze_tournament(results, candidates, opponents, min_seed_blocks=1)
