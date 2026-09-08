import pytest

from scripts.verify_ray_cluster import assert_identical


def result(hostname, *, money=1.5, opponent_money=-0.0, score=1):
    return {'hostname': hostname, 'rows': [{
        'job_id': 'job-1', 'money': money, 'opponent_money': opponent_money,
        'score': score, 'winner': 0, 'runtime_ms': 1, 'wall_seconds': .1,
        'hostname': hostname,
    }]}


def test_determinism_evidence_records_full_and_binary64_digests_per_node():
    evidence = assert_identical([
        ({'NodeID': 'node-a'}, result('pc-a')),
        ({'NodeID': 'node-b'}, result('pc-b')),
    ])

    assert [item['node_id'] for item in evidence] == ['node-a', 'node-b']
    assert evidence[0]['relevant_result_sha256'] == evidence[1]['relevant_result_sha256']
    assert evidence[0]['money_binary64_sha256'] == evidence[1]['money_binary64_sha256']


def test_signed_zero_money_difference_is_a_binary64_hard_failure():
    with pytest.raises(SystemExit, match='Binary64 money mismatch'):
        assert_identical([
            ({'NodeID': 'node-a'}, result('pc-a', opponent_money=-0.0)),
            ({'NodeID': 'node-b'}, result('pc-b', opponent_money=0.0)),
        ])


def test_any_other_relevant_result_difference_is_a_hard_failure():
    with pytest.raises(SystemExit, match='Bit-exact result mismatch'):
        assert_identical([
            ({'NodeID': 'node-a'}, result('pc-a', score=1)),
            ({'NodeID': 'node-b'}, result('pc-b', score=0)),
        ])
