import json

import pytest

from arena.match import run_match
from arena.engine import make_environment, official
from arena.agents import load_agent, invoke
from arena.match import observations
from agent.economy import price


@pytest.mark.parametrize('seed,seat,opponent', [(3, 0, 'starter'), (17, 1, 'animal'), (41, 0, 'diversified')])
def test_fast_matches_official_every_turn(tmp_path, seed, seat, opponent):
    fast = tmp_path / 'fast.json'
    reference = tmp_path / 'official.json'
    a = run_match('challenger', opponent, seed, seat, replay=fast)
    b = run_match('challenger', opponent, seed, seat, backend='official', replay=reference)
    assert not a['failures'] and not b['failures']
    assert a['money'] == b['money']
    assert a['opponent_money'] == b['opponent_money']
    assert a['steps'] == b['steps'] == 719
    assert json.loads(fast.read_text())['turns'] == json.loads(reference.read_text())['turns']


def test_seeded_random_reproducible():
    a = run_match('starter', 'random', 99)
    b = run_match('starter', 'random', 99)
    for key in ('score', 'money', 'opponent_money', 'audit', 'opponent_audit'):
        assert a[key] == b[key]


def test_price_model_matches_official():
    module = official()
    for item in module.PRODUCTS:
        for inventory in (0, 9000, 9500, 9900, 9999, 10000, 10001, 10020, 10100, 11000):
            assert price(item, inventory) == module.market_price(item, inventory)


def test_plant_must_be_watered_before_night():
    module = official()
    plant = module._new_plant('CARROT', 0, 24)
    farm = {'tiles': [[plant]]}
    module._daily_refresh_plants(farm, 0, 24)
    assert farm['tiles'][0][0]['kind'] == 'WEED'


def test_observations_are_private_and_detached():
    env = make_environment(2)
    obs = observations(env.state)
    assert 'private' not in obs[0]['farms'][1]
    obs[0]['private']['shed']['WHEAT'] = 900
    obs[0]['farms'][0]['money'] = -5
    assert env.state[0].observation.private['shed'].get('WHEAT', 0) == 0
    assert obs[1]['farms'][0]['money'] == 3000
