"""Pinned-engine semantics and the isolated market-slot reservation policy (#26)."""

from agent.economy import price
from agent.market import schedule_market_orders
from agent.params import DEFAULTS
from agent.planner import policy
from arena.engine import make_environment, official
from arena.match import observations


IDLE = {'farmer': ['PASS'], 'hands': [], 'market': []}


def _market_env(limit=2, seed=26):
    env = make_environment(seed, {'maxMarketOrdersPerTurn': limit})
    shared = env.state[0].observation
    for seat in (0, 1):
        shared.farms[seat].money = 0
        env.state[seat].observation.private.shed['WHEAT'] = 1
    return env


def test_engine_resolves_positions_in_order_and_continues_after_failure():
    sell_first = _market_env()
    inventory = sell_first.state[0].observation.market.inventory['WHEAT']
    quote = official().market_price('WHEAT', inventory)
    sell_first.step([
        {'farmer': ['PASS'], 'hands': [], 'market': [
            ['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]},
        IDLE,
    ])
    # Selling first funds the following buy at the engine's round-trip price.
    assert sell_first.state[0].observation.private.shed['WHEAT'] == 1
    assert sell_first.state[0].observation.farms[0].money == 0

    buy_first = _market_env()
    buy_first.step([
        {'farmer': ['PASS'], 'hands': [], 'market': [
            ['BUY_PRODUCT', 'WHEAT', 1], ['SELL', 'WHEAT', 1]]},
        IDLE,
    ])
    # The unaffordable buy fails, but the later sale still executes.
    assert buy_first.state[0].observation.private.shed['WHEAT'] == 0
    assert buy_first.state[0].observation.farms[0].money == quote


def test_engine_truncates_before_resolving_market_orders():
    env = _market_env(limit=1)
    env.state[0].observation.farms[0].money = 100
    env.step([
        {'farmer': ['PASS'], 'hands': [], 'market': [
            ['SELL', 'WHEAT', 1], ['HIRE']]},
        IDLE,
    ])
    assert env.state[0].observation.private.shed['WHEAT'] == 0
    assert env.state[0].observation.farms[0].hands == []


def test_engine_quotes_opponents_in_lockstep_at_each_position():
    env = _market_env(limit=1)
    env.state[0].observation.market.inventory['WHEAT'] = 9900
    inventory = env.state[0].observation.market.inventory['WHEAT']
    quote = official().market_price('WHEAT', inventory)
    sell = {'farmer': ['PASS'], 'hands': [], 'market': [['SELL', 'WHEAT', 1]]}
    env.step([sell, sell])
    assert [farm.money for farm in env.state[0].observation.farms] == [quote, quote]
    assert [env.state[seat].observation.private.shed['WHEAT'] for seat in (0, 1)] == [0, 0]


def test_scheduler_reserves_only_requested_slots_and_keeps_sales_first():
    assert DEFAULTS['market_slot_reservation'] is True
    sales = [['SELL', 'MELON', 8], ['SELL', 'WOOL', 4], ['SELL', 'EGG', 2]]
    essential = [['HIRE'], ['BUY_SEED', 'CARROT', 3]]
    optional = [['BUY_ANIMAL', 'GOOSE', 1]]
    assert schedule_market_orders(sales, essential, optional, limit=3) == [
        ['SELL', 'MELON', 8], ['HIRE'], ['BUY_SEED', 'CARROT', 3]]
    assert schedule_market_orders(sales, [], optional, limit=3) == sales


def _sale_pressure_observation(env, hour):
    obs = observations(env.state)[0]
    obs.update(step=hour, day=0, hour=hour)
    obs['private']['shed']['MELON'] = 40
    obs['market']['inventory']['MELON'] = 9000
    return obs


def test_policy_reserves_one_slot_for_an_economically_accepted_hire():
    env = make_environment(260, {'maxMarketOrdersPerTurn': 1})
    obs = _sale_pressure_observation(env, hour=0)
    action = policy(obs, dict(env.configuration))
    assert action['market'] == [['HIRE']]
    env.step([action, IDLE])
    assert len(env.state[0].observation.farms[0].hands) == 1

    control = policy(obs, dict(env.configuration), {'market_slot_reservation': False})
    assert control['market'][0][0] == 'SELL'


def test_policy_reserves_one_slot_for_planned_seed_shortage():
    env = make_environment(261, {'maxMarketOrdersPerTurn': 1})
    obs = _sale_pressure_observation(env, hour=4)
    action = policy(obs, dict(env.configuration))
    assert action['market'][0][0] == 'BUY_SEED'
    crop = action['market'][0][1]
    env.step([action, IDLE])
    assert env.state[0].observation.private.seeds[crop] > 0


def test_policy_reserves_one_slot_for_required_feed_product():
    env = make_environment(262, {'maxMarketOrdersPerTurn': 1})
    obs = _sale_pressure_observation(env, hour=4)
    obs['farms'][0]['tiles'][0][0] = {
        'animal': 'COW', 'fed_today': False, 'cared_today': False,
        'consecutive_unfed': 0, 'yield_units': 0, 'fertilizer_available': False,
    }
    action = policy(obs, dict(env.configuration), {
        'plant_until_hour': 0, 'planned_feedback': True})
    assert action['market'] == [['BUY_PRODUCT', 'WHEAT', 2]]
    env.step([action, IDLE])
    assert env.state[0].observation.private.shed['WHEAT'] == 2
