import json

import pytest

from scripts.benchmark_ray import load_verification


def proof():
    return {
        'schema_version': 3,
        'paired_seats': True,
        'bit_exact': True,
        'money_binary64_exact': True,
        'deadline_passed_on_every_node': True,
        'worker_recovery_passed': True,
        'candidate': 'candidate.py',
        'opponent': 'opponent.py',
        'hostnames': ['pc-a', 'pc-b'],
        'driver_git': {'git_commit': 'abc123'},
        'jobs_per_node': 400,
        'seed_pairs': 200,
        'determinism_nodes': [
            {'hostname': host, 'relevant_result_sha256': 'results',
             'money_binary64_sha256': 'money'} for host in ('pc-a', 'pc-b')
        ],
        'worker_recovery_nodes': [
            {'hostname': host, 'attempts': 2} for host in ('pc-a', 'pc-b')
        ],
    }


def write(tmp_path, value):
    path = tmp_path / 'verification.json'
    path.write_text(json.dumps(value), encoding='utf-8')
    return path


def load(path, **changes):
    arguments = {'candidate': 'candidate.py', 'opponent': 'opponent.py',
                 'hostnames': ['pc-a', 'pc-b'],
                 'current_git': {'git_commit': 'abc123'}}
    arguments.update(changes)
    return load_verification(path, **arguments)


def test_benchmark_binds_the_exact_verification_artifact(tmp_path):
    path = write(tmp_path, proof())
    evidence = load(path)
    assert evidence['git_commit'] == 'abc123'
    assert evidence['hostnames'] == ['pc-a', 'pc-b']
    assert evidence['jobs_per_node'] == 400
    assert len(evidence['sha256']) == 64


@pytest.mark.parametrize('mutation, message', [
    (lambda value: value.update(money_binary64_exact=False), 'release gate'),
    (lambda value: value.update(candidate='other.py'), 'benchmark agents'),
    (lambda value: value.update(hostnames=['pc-a']), 'current cluster'),
    (lambda value: value.update(seed_pairs=1, jobs_per_node=2), '200 seeds'),
    (lambda value: value['driver_git'].update(git_commit='old'), 'git commit'),
    (lambda value: value['worker_recovery_nodes'].pop(), 'every current hostname'),
    (lambda value: value['determinism_nodes'][1].update(
        money_binary64_sha256='different'), 'digests'),
])
def test_stale_or_incomplete_verification_is_a_hard_failure(tmp_path, mutation, message):
    value = proof()
    mutation(value)
    with pytest.raises(SystemExit, match=message):
        load(write(tmp_path, value))
