import copy
import json
import random

import pytest

from arena.match import run_match
from experiments.block_solver import arrival_state, block_end, fitness, mutations, search


def tape():
    actions = [dict(farmer=['PASS'], hands=[], market=[]) for _ in range(719)]
    for turn in range(648, 719):
        actions[turn]['market'] = [['SELL', 'WHEAT', 12], ['SELL', 'WOOL', 6]]
    return actions


def test_blocks_align_with_shop_boundaries_and_terminal_truncation():
    assert block_end(72) == 144
    assert block_end(144, 6) == 288
    assert block_end(648) == 719
    for start, days in [(1, 3), (-72, 3), (720, 3), (0, 4)]:
        with pytest.raises(ValueError):
            block_end(start, days)


def test_mutations_are_deterministic_local_and_do_not_alias_inputs():
    original = tape()
    before = copy.deepcopy(original)
    variants = mutations(original, 648, 719, 20, random.Random(7))
    assert variants == mutations(original, 648, 719, 20, random.Random(7))
    assert len({variant['sha256'] for variant in variants}) == 20
    for variant in variants:
        assert variant['actions'][:648] == original[:648]
        assert all(a['farmer'] == b['farmer'] and a['hands'] == b['hands']
                   for a, b in zip(variant['actions'], original))
        assert all(len(action['market']) <= 10 for action in variant['actions'])
        variant['actions'][0]['farmer'].append('changed')
    assert original == before


def test_no_available_edit_returns_empty_without_fabricating_a_candidate():
    actions = [dict(farmer=['PASS'], hands=[], market=[]) for _ in range(719)]
    assert mutations(actions, 0, 72, 4, random.Random(1)) == []


def test_fitness_ignores_coins_and_prefers_the_worst_opponent():
    steady = [dict(opponent='a', score=.5, margin=0), dict(opponent='b', score=.5, margin=0)]
    spiky = [dict(opponent='a', score=1, margin=100000), dict(opponent='b', score=0, margin=100000)]
    assert fitness(steady) > fitness(spiky)
    for row in steady:
        row['margin'] = -10000000
    assert fitness(steady) == (.5, .5)


def test_arrival_preserves_locations_ages_and_separate_inventories():
    obs = dict(player=0, step=72, day=3, hour=0, market={}, town={},
               farms=[dict(money=2, farmer=[1, 2], hands=[[3, 4]],
                           tiles=[[dict(crop='WHEAT', age=2)]])],
               private=dict(shed={'WHEAT': 5}, inventories=[{'WOOL': 1}, {'WOOL': 2}]))
    first = arrival_state(obs, 0)
    obs['farms'][0]['tiles'][0][0]['age'] = 3
    assert first['sha256'] != arrival_state(obs, 0)['sha256']
    assert first['state']['farm']['tiles'][0][0]['age'] == 2
    assert first['state']['private']['inventories'] == [{'WOOL': 1}, {'WOOL': 2}]
    with pytest.raises(ValueError, match='different seat'):
        arrival_state(obs, 1)


def test_search_rejects_validation_holdout_and_overlap_before_output(tmp_path):
    source = tmp_path / 'tapes.json'
    source.write_text(json.dumps([tape()]))
    for seeds, check in [([1000, 1001], [1001, 1002]),
                         ([100125, 100126], [1000, 1001]),
                         ([9000000, 9000001], [1000, 1001])]:
        with pytest.raises(ValueError):
            search(source, tmp_path / 'out', opponents=['starter'], seeds=seeds, check_seeds=check)
        assert not (tmp_path / 'out').exists()


def test_sparse_snapshots_preserve_real_match_outcome_and_boundary_clock(tmp_path):
    before = run_match('pass', 'starter', 12, seat=1, telemetry_enabled=False)
    path = tmp_path / 'snapshots.json'
    after = run_match('pass', 'starter', 12, seat=1, telemetry_enabled=False,
                      replay=path, replay_steps=[0, 72, 144, 719])
    for key in ('score', 'money', 'margin', 'candidate_hash', 'environment'):
        assert before[key] == after[key]
    replay = json.loads(path.read_text())
    assert replay['format'] == 'kaggriculture-lab-snapshots-v1'
    assert [turn['step'] for turn in replay['turns']] == [0, 72, 144, 719]
    for turn in replay['turns']:
        assert turn['observations'][1]['step'] == turn['step']


@pytest.mark.parametrize('steps', [[], [1, 1], [-1], [True], [720]])
def test_invalid_snapshot_steps_are_rejected(tmp_path, steps):
    with pytest.raises(ValueError):
        run_match('pass', 'pass', 1, replay=tmp_path / 'bad.json', replay_steps=steps)


def test_search_freezes_before_disjoint_check_and_keeps_incumbent_on_ties(tmp_path, monkeypatch):
    from experiments import block_solver as solver
    source = tmp_path / 'source.json'
    source.write_text(json.dumps([tape()]))
    output = tmp_path / 'out'
    calls = []
    def evaluate(actions, directory, *, seeds, **kwargs):
        directory.mkdir()
        artifact = directory / 'main.py'
        artifact.write_text('def agent(obs): return {}\n')
        is_check = 'check' in directory.name
        if is_check:
            assert (output / 'selection.json').is_file()
            assert list(seeds) == [1002, 1003]
        else:
            assert list(seeds) == [1000, 1001]
        if directory.name != 'baseline-search' and directory.name != 'baseline-check':
            assert kwargs['expected_frontiers'] == {'test': 'frontier'}
        calls.append(directory.name)
        rows = [dict(seed=seed, seat=seat, opponent='starter', score=.5, margin=0,
            candidate_hash='same', opponent_hash='opponent', environment={}, configuration={},
            backend='fast', failures=[], opponent_failures=[]) for seed in seeds for seat in (0, 1)]
        return dict(rows=rows, frontiers={'test': 'frontier'}, fitness=(.5, .5),
                    artifact=str(artifact), artifact_hash='same')
    monkeypatch.setattr(solver, 'evaluate', evaluate)
    monkeypatch.setattr(solver, 'engine_fingerprint', lambda: {})
    result = solver.search(source, output, opponents=['starter'], seeds=[1000, 1001],
                           check_seeds=[1002, 1003], proposals=2, rounds=1)
    assert result['accepted_mutations'] == []
    assert calls[-2:] == ['baseline-check', 'candidate-check']
    assert result['release_status'] == 'not_validated'
    emitted = json.loads((output / 'tapes.json').read_text())
    assert emitted['tapes'][0]['actions'] == tape()


def test_candidate_with_different_frontier_is_refused(tmp_path, monkeypatch):
    from experiments import block_solver as solver
    def matches(jobs, workers):
        for job in jobs:
            obs = dict(player=job['seat'], step=648, day=27, hour=0, farms=[], private={})
            from pathlib import Path
            Path(job['replay']).write_text(json.dumps({'turns': [
                dict(step=step, observations=[obs, obs]) for step in (648, 719)]}))
            yield dict(candidate_hash=solver.agent_hash(job['candidate']), opponent_hash='x',
                       failures=[], opponent_failures=[], seat=job['seat'], seed=job['seed'],
                       opponent=job['opponent'])
    monkeypatch.setattr(solver, 'matches', matches)
    with pytest.raises(ValueError, match='same frontier'):
        solver.evaluate(tape(), tmp_path / 'trial', ['starter'], [1000], 648, 719, 1,
                        'unit test', expected_frontiers={})
