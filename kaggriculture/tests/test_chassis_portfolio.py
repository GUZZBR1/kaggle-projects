"""The chassis comes from a pinned third-party bundle, so the seam has to hold.

Two things can go wrong silently here and both would be invisible on the ladder.
The build can cut the upstream file in the wrong place, shipping a truncated
chassis that still imports; and a routing stage can fire from a route whose state
its alternatives were never written to follow, which is the defect this module's
`when` guard exists to prevent.
"""
import json

import pytest

from arena.agents import load_agent
from experiments import chassis_portfolio
from experiments.chassis_portfolio import build, prelude


LAYERS_OFF = {name: False for name in
              ('hand_align', 'weed_repair', 'sell_lead', 'front_run', 'budget_guard',
               'room_guard', 'clamp_sells', 'dead_stock', 'terminal_liquidation')}


def stream(marker, n=719):
    return [{'farmer': [marker], 'hands': [], 'market': []} for _ in range(n)]


def observation(step=0, shops=(), egg=10000):
    farms = [{'money': 100, 'tiles': [[None, None], [None, None]], 'unlocked_quadrants': ['NW'],
              'farmer': [0, 0], 'hands': [], 'hires_today': 0},
             {'money': 100, 'tiles': [[None, None], [None, None]], 'unlocked_quadrants': ['NW'],
              'farmer': [0, 0], 'hands': [], 'hires_today': 0}]
    return {'step': step, 'day': step // 24, 'hour': step % 24, 'player': 0, 'farms': farms,
            'private': {'shed': {}, 'seeds': {}, 'inventories': [{}]},
            'town': {'unlocked_shops': list(shops)},
            'market': {'prices': {'WHEAT': 25}, 'inventory': {'EGG': egg}}}


def test_the_chassis_is_taken_whole_from_the_pinned_bundle():
    """A wrong cut would ship a chassis that still imports and quietly misbehaves."""
    text = prelude()
    assert text.startswith('# SPDX-License-Identifier: Apache-2.0')
    assert 'Apache License' in text, 'the licence text must travel with the code'
    assert 'class Chassis' in text and text.rstrip().endswith('return agent')
    assert chassis_portfolio.PAYLOAD_MARKER not in text


def test_a_stage_may_not_route_or_guard_outside_the_portfolio(tmp_path):
    tapes = [stream('NORTH'), stream('SOUTH')]
    with pytest.raises(ValueError, match='outside the portfolio'):
        build(tapes, [(72, 'shop_count', 'BAKERY', 0, 5, 0)], tmp_path / 'a.py')
    with pytest.raises(ValueError, match='guards on a route'):
        build(tapes, [(72, 'shop_count', 'BAKERY', 0, 1, 0, (7,))], tmp_path / 'b.py')
    with pytest.raises(ValueError, match='Unknown routing feature'):
        build(tapes, [(72, 'rival_money', 'BAKERY', 0, 1, 0)], tmp_path / 'c.py')
    with pytest.raises(ValueError, match='719'):
        build([stream('NORTH', 700)], [], tmp_path / 'd.py')


def test_a_guarded_stage_never_fires_from_a_route_it_does_not_vary(tmp_path):
    """The upstream defect: tapes 2 and 3 vary tape 0 only, but the terminal stage
    fired from any route, splicing a foreign season plan into the last three days."""
    tapes = [stream('NORTH'), stream('SOUTH'), stream('EAST')]
    stages = [(72, 'shop_count', 'YARN_STORE', .5, 1, 0),
              (144, 'market_inventory', 'EGG', 9888, 2, 0, (0,))]
    path = build(tapes, stages, tmp_path / 'guarded.py', settings=LAYERS_OFF)
    agent = load_agent(str(path))

    # Yarn store present: route 1, and the guarded terminal stage must not fire.
    assert agent(observation(step=0))['farmer'] == ['NORTH']
    assert agent(observation(step=72, shops=('YARN_STORE',)))['farmer'] == ['SOUTH']
    assert agent(observation(step=144, shops=('YARN_STORE',), egg=10000))['farmer'] == ['SOUTH']

    # No yarn store: route stays 0, so the terminal stage is allowed to fire.
    other = load_agent(str(build(tapes, stages, tmp_path / 'guarded2.py', settings=LAYERS_OFF)))
    assert other(observation(step=0))['farmer'] == ['NORTH']
    assert other(observation(step=72))['farmer'] == ['NORTH']
    assert other(observation(step=144, egg=10000))['farmer'] == ['EAST']


def test_a_stage_latches_once_and_holds_its_choice(tmp_path):
    """A decision belongs to the world at the step it was fitted for, not to a
    later swing in the same feature."""
    tapes = [stream('NORTH'), stream('SOUTH')]
    stages = [(72, 'shop_count', 'YARN_STORE', .5, 1, 0)]
    agent = load_agent(str(build(tapes, stages, tmp_path / 'latch.py', settings=LAYERS_OFF)))

    assert agent(observation(step=72, shops=('YARN_STORE',)))['farmer'] == ['SOUTH']
    assert agent(observation(step=144))['farmer'] == ['SOUTH']


def test_both_self_play_seats_keep_independent_route_state(tmp_path):
    tapes = [stream('NORTH'), stream('SOUTH')]
    stages = [(72, 'shop_count', 'YARN_STORE', .5, 1, 0)]
    agent = load_agent(str(build(tapes, stages, tmp_path / 'seats.py', settings=LAYERS_OFF)))

    seat_one = observation(step=72, shops=('YARN_STORE',))
    seat_one['player'] = 1
    assert agent(observation(step=72))['farmer'] == ['NORTH']
    assert agent(seat_one)['farmer'] == ['SOUTH']
    assert agent(observation(step=144))['farmer'] == ['NORTH']
