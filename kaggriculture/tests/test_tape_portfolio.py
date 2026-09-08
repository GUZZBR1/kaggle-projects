"""A portfolio is several tapes plus a rule; both halves have to survive the build."""
import json

import pytest

from arena.agents import load_agent
from experiments.tape_portfolio import FEATURE_NAMES, build, features


def stream(marker, n=719):
    return [{'farmer': [marker], 'hands': [], 'market': [['SELL', 'WHEAT', 1]]}
            for _ in range(n)]


def observation(shops=(), money=(100, 50), step=0):
    tiles = [[None] * 2 for _ in range(2)]
    tiles[0][0] = {'kind': 'PLANT', 'crop': 'WHEAT'}
    farms = [{'money': money[0], 'tiles': tiles, 'unlocked_quadrants': ['NW'],
              'farmer': [0, 0], 'hands': []},
             {'money': money[1], 'tiles': [[None]], 'unlocked_quadrants': [],
              'farmer': [0, 0], 'hands': []}]
    return {'step': step, 'day': step // 24, 'hour': step % 24, 'player': 0, 'farms': farms,
            'town': {'unlocked_shops': list(shops)},
            'market': {'prices': {'WHEAT': 25}, 'inventory': {'WHEAT': 9000}}}


def test_the_feature_vector_matches_its_documented_names():
    """Rules are fitted against indices, so the order is part of the contract."""
    assert len(features(observation())) == len(FEATURE_NAMES)
    vector = features(observation(shops=('BAKERY', 'BAKERY', 'YARN_STORE')))
    assert vector[FEATURE_NAMES.index('shop_bakery')] == 2
    assert vector[FEATURE_NAMES.index('shops_total')] == 3
    assert vector[FEATURE_NAMES.index('money_lead')] == 50
    assert vector[FEATURE_NAMES.index('own_wheat')] == 1
    assert vector[FEATURE_NAMES.index('rival_wheat')] == 0


def test_a_portfolio_needs_whole_and_equal_length_tapes(tmp_path):
    with pytest.raises(ValueError, match='719'):
        build([stream('NORTH', 100)], {}, tmp_path / 'short.py')
    with pytest.raises(ValueError, match='same number'):
        build([stream('NORTH'), stream('SOUTH', 700)], {}, tmp_path / 'ragged.py')
    with pytest.raises(ValueError, match='at least one'):
        build([], {}, tmp_path / 'empty.py')


def test_a_rule_may_not_route_outside_the_portfolio(tmp_path):
    with pytest.raises(ValueError, match='outside'):
        build([stream('NORTH'), stream('SOUTH')], {1: [[8, 0, 5, -1]]}, tmp_path / 'bad.py')
    with pytest.raises(ValueError, match='feature, cut'):
        build([stream('NORTH')], {1: [[8, 0]]}, tmp_path / 'bad.py')


def test_routing_happens_only_at_block_boundaries(tmp_path):
    """The town reveals a shop every three days, so mid-block switching is noise."""
    path = build([stream('NORTH'), stream('SOUTH')], {1: [[8, 0, 1, -1]]}, tmp_path / 'p.py')
    agent = load_agent(str(path))

    assert agent(observation(step=0))['farmer'] == ['NORTH']
    # A shop appears mid-block: the commitment holds until the boundary at 72.
    assert agent(observation(shops=('BAKERY',), step=40))['farmer'] == ['NORTH']
    assert agent(observation(shops=('BAKERY',), step=72))['farmer'] == ['SOUTH']
    # The rule does not fire again once its block is past, so the route persists.
    assert agent(observation(step=144))['farmer'] == ['SOUTH']


def test_an_unmatched_rule_keeps_the_running_route(tmp_path):
    path = build([stream('NORTH'), stream('SOUTH')], {1: [[8, 0, 1, -1]]}, tmp_path / 'p.py')
    agent = load_agent(str(path))
    assert agent(observation(step=0))['farmer'] == ['NORTH']
    assert agent(observation(step=72))['farmer'] == ['NORTH'], 'no shops, no switch'


def test_both_self_play_seats_keep_independent_commitments(tmp_path):
    path = build([stream('NORTH'), stream('SOUTH')], {1: [[8, 0, 1, -1]]}, tmp_path / 'p.py')
    agent = load_agent(str(path))
    seat_one = observation(shops=('BAKERY',), step=72)
    seat_one['player'] = 1
    seat_one['farms'] = list(reversed(seat_one['farms']))
    assert agent(observation(step=0))['farmer'] == ['NORTH']
    assert agent(seat_one)['farmer'] == ['SOUTH']
    assert agent(observation(step=24))['farmer'] == ['NORTH'], 'seat 0 is untouched'


def test_out_of_range_turns_fall_back_to_pass(tmp_path):
    agent = load_agent(str(build([stream('NORTH')], {}, tmp_path / 'p.py')))
    for turn in (-1, 719, 5000):
        assert agent({'step': turn}) == {'farmer': ['PASS'], 'hands': [], 'market': []}
