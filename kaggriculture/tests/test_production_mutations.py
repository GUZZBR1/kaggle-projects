import copy
import random

import pytest

from experiments.production_mutations import production_mutations, WORK
from experiments.tape_harvest import tape_digest


def tape():
    actions = [dict(farmer=['NORTH'], hands=[['EAST']], market=[['HIRE']]) for _ in range(719)]
    actions[144]['farmer'] = ['PASS']
    actions[145]['farmer'] = ['HARVEST']
    actions[144]['hands'][0] = ['WATER']
    actions[145]['hands'][0] = ['PLANT', 'WHEAT']
    return actions


def test_idle_hypotheses_cover_production_and_keep_market_routes_and_boundaries():
    initial = tape()
    saved = copy.deepcopy(initial)
    variants = production_mutations(initial, 144, 288, 6, random.Random(7))
    assert [v['mutation']['work'] for v in variants] == list(WORK)
    for variant in variants:
        actions = variant['actions']
        assert actions[:144] == initial[:144] and actions[288:] == initial[288:]
        assert [a['market'] for a in actions] == [a['market'] for a in initial]
        assert [a['hands'] for a in actions] == [a['hands'] for a in initial]
        assert actions[144]['farmer'] == [variant['mutation']['work']]
        assert actions[145:] == initial[145:]
        actions[144]['market'].append(['PASS'])
    assert initial == saved


def test_work_swaps_preserve_arguments_and_worker_identity():
    initial = tape()
    variants = production_mutations(initial, 144, 288, 30, random.Random(7))
    swap = next(v for v in variants if v['mutation']['kind'] == 'swap_work'
                and v['mutation']['role'] == 'hands')
    assert swap['actions'][144]['hands'] == [['PLANT', 'WHEAT']]
    assert swap['actions'][145]['hands'] == [['WATER']]
    assert swap['actions'][144]['farmer'] == ['PASS']
    assert swap['actions'][146] == initial[146]


def test_generation_is_deterministic_unique_and_fills_budget_past_visited_candidates():
    initial = tape()
    a = production_mutations(initial, 144, 288, 6, random.Random(7))
    assert a == production_mutations(initial, 144, 288, 6, random.Random(7))
    blocked = {v['sha256'] for v in a}
    b = production_mutations(initial, 144, 288, 2, random.Random(7), excluded=blocked)
    assert len(b) == 2
    assert not blocked & {v['sha256'] for v in b}
    assert all(tape_digest(v['actions']) == v['sha256'] for v in b)


def test_never_swaps_across_block_or_missing_worker():
    actions = tape()
    actions[145]['hands'] = []
    variants = production_mutations(actions, 144, 145, 30, random.Random(7))
    assert all(v['mutation']['kind'] != 'swap_work' for v in variants)
    variants = production_mutations(actions, 144, 288, 30, random.Random(7))
    assert all(v['mutation'].get('role') != 'hands' for v in variants)


def test_market_search_also_fills_budget_after_excluding_previous_proposals():
    from experiments.block_solver import mutations
    actions = tape()
    for a in actions[144:288]:
        a['market'] = [['SELL', 'WHEAT', 4], ['SELL', 'WOOL', 8]]
    a = mutations(actions, 144, 288, 4, random.Random(7))
    excluded = {v['sha256'] for v in a}
    b = mutations(actions, 144, 288, 4, random.Random(7), excluded=excluded)
    assert len(b) == 4
    assert not excluded & {v['sha256'] for v in b}


def test_unknown_search_space_is_rejected_before_reading_source(tmp_path):
    from experiments.block_solver import search
    with pytest.raises(ValueError, match='Unknown mutation space'):
        search(tmp_path / 'missing.json', tmp_path / 'out', mutation_space='unknown',
               opponents=['starter'], seeds=[1000, 1001], check_seeds=[1002, 1003])
    assert not (tmp_path / 'out').exists()
