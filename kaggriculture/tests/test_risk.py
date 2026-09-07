import math

import pytest

from agent.planner import policy
from agent.state import State
from arena.engine import make_environment
from arena.match import observations


def state(step=600, own=12_000, opponent=10_000, player=0):
    money = [own, opponent] if player == 0 else [opponent, own]
    return State(
        {'step': step, 'day': step // 24, 'hour': step % 24, 'player': player,
         'farms': [{'money': value} for value in money]},
        {'episodeSteps': 720, 'turnsPerDay': 24},
    )


@pytest.mark.parametrize(
    'own,opponent,expected',
    [(12_000, 10_000, 'ahead'), (11_000, 10_000, 'neutral'),
     (8_000, 10_000, 'behind')],
)
def test_risk_posture_uses_public_cash_with_deadband(own, opponent, expected):
    assert state(own=own, opponent=opponent).risk_posture() == expected


def test_risk_posture_is_seat_relative_and_limited_to_final_five_days():
    assert state(player=1).risk_posture() == 'ahead'
    assert state(step=599).risk_posture() == 'ahead'
    assert state(step=598).risk_posture() == 'neutral'


@pytest.mark.parametrize('value', [None, True, math.nan, math.inf, 'unknown'])
def test_risk_posture_fails_safe_for_invalid_public_money(value):
    assert state(own=value).risk_posture() == 'neutral'
    assert state(opponent=value).risk_posture() == 'neutral'


def endgame_observation(own, opponent):
    env = make_environment(3)
    obs = observations(env.state)[0]
    obs.update(step=600, day=25, hour=0)
    obs['farms'][0]['money'] = own
    obs['farms'][1]['money'] = opponent
    return obs, dict(env.configuration)


def test_ahead_preserves_existing_crop_and_sales_without_new_seed_buys():
    obs, config = endgame_observation(12_000, 10_000)
    x, y = obs['farms'][0]['farmer']
    obs['farms'][0]['tiles'][y][x] = {
        'kind': 'PLANT', 'crop': 'WHEAT', 'planted_day': 24,
        'watered_today': False, 'consecutive_unwatered': 1, 'yield_units': 0,
    }
    obs['private']['shed']['CARROT'] = 3
    action = policy(obs, config)

    assert action['farmer'] == ['WATER']
    assert ['SELL', 'CARROT', 3] in action['market']
    assert not any(order[0] == 'BUY_SEED' for order in action['market'])


def test_behind_can_spend_the_cash_reserve_on_viable_endgame_seed():
    obs, config = endgame_observation(245, 2_000)
    action = policy(obs, config, {'max_hands': 0})

    assert ['BUY_SEED', 'CARROT', 12] in action['market']
