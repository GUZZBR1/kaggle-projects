import pytest

from scripts.benchmark_pool import add_scaling, result_signature


def test_scaling_uses_each_modes_own_one_worker_baseline():
    rows = [
        {'mode': 'direct', 'workers': 1, 'seconds': 12.0},
        {'mode': 'batched', 'workers': 1, 'seconds': 10.0},
        {'mode': 'direct', 'workers': 4, 'seconds': 3.0},
        {'mode': 'batched', 'workers': 4, 'seconds': 2.0},
    ]

    add_scaling(rows)

    assert rows[2]['speedup_vs_one_worker'] == 4.0
    assert rows[2]['parallel_efficiency'] == 1.0
    assert rows[3]['speedup_vs_one_worker'] == 5.0
    assert rows[3]['parallel_efficiency'] == 1.25


def test_scaling_requires_a_one_worker_baseline_for_every_mode():
    with pytest.raises(ValueError, match='batched'):
        add_scaling([{'mode': 'batched', 'workers': 4, 'seconds': 2.0}])


def test_result_signature_is_exact_but_ignores_only_execution_metadata():
    base = {'seed': 1, 'score': 1., 'money': 10., 'opponent_money': 9.,
            'audit': {'sell': 2}, 'runtime_ms': [1.], 'wall_seconds': .2}
    transported = {**base, 'runtime_ms': [9.], 'wall_seconds': .8,
                   'hostname': 'worker', 'job_id': 'j', 'batch_id': 'b'}
    assert result_signature([base]) == result_signature([transported])
    assert result_signature([base]) != result_signature([{**base, 'opponent_money': 9.0000001}])
