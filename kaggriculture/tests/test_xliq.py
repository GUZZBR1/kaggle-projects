import copy

from agent.xliq import opening_treatment, wrap_agent
from arena.agents import load_agent


def observation(day=0):
    farm = {'money': 3000, 'farmer': [0, 0], 'hands': [],
            'tiles': [[None, None], [None, None]], 'unlocked_quadrants': [0],
            'hires_today': 0}
    private = {'seeds': {'WHEAT': 2, 'STRAWBERRY': 1},
               'shed': {'WHEAT': 0, 'STRAWBERRY': 0},
               'inventories': [{'WHEAT': 0, 'STRAWBERRY': 0}]}
    return {'day': day, 'hour': 0, 'player': 0, 'farms': [farm, copy.deepcopy(farm)],
            'private': private}


def action():
    return {'farmer': ['PLANT', 'MELON'], 'hands': [],
            'market': [['HIRE'], ['BUY_SEED', 'MELON', 20], ['BUY_LAND']]}


def test_treatment_is_exactly_the_base_after_opening():
    original = action()
    assert opening_treatment(original, observation(day=3), {}) is original


def test_treatment_changes_only_opening_plants_and_seed_purchases():
    original = action()
    treated = opening_treatment(original, observation(), {'maxMarketOrdersPerTurn': 10})
    assert original == action(), 'the frozen base action must remain untouched'
    assert treated['farmer'][0] == 'PLANT'
    assert treated['farmer'][1] in ('WHEAT', 'STRAWBERRY')
    assert treated['market'][0] == ['HIRE'] and treated['market'][-1] == ['BUY_LAND']
    seed_orders = [order for order in treated['market'] if order[0] == 'BUY_SEED']
    assert seed_orders == [['BUY_SEED', 'WHEAT', 4], ['BUY_SEED', 'STRAWBERRY', 1]]
    assert sum(order[2] * {'WHEAT': 10, 'STRAWBERRY': 100}[order[1]]
               for order in seed_orders) <= 2000


def test_wrapper_calls_frozen_base_once_and_accepts_step_none():
    calls = []
    def base(obs, config=None):
        calls.append(obs)
        return action()
    obs = observation()
    obs['step'] = None
    wrapped = wrap_agent(base)
    assert wrapped(obs, {})['farmer'][0] == 'PLANT'
    assert calls == [obs]


def test_capital_floor_accounts_for_retained_base_purchases():
    obs = observation()
    obs['farms'][0]['money'] = 1500
    treated = opening_treatment(action(), obs, {'maxMarketOrdersPerTurn': 10})
    assert ['BUY_LAND'] not in treated['market']
    costs = {'HIRE': 1, 'BUY_SEED': {'WHEAT': 10, 'STRAWBERRY': 100}}
    spent = sum(costs['HIRE'] if order[0] == 'HIRE'
                else costs['BUY_SEED'][order[1]] * order[2]
                for order in treated['market'])
    assert obs['farms'][0]['money'] - spent >= 1000


def test_clock_adapter_derives_missing_or_none_step_without_touching_base_file(tmp_path):
    base = tmp_path / 'step_agent.py'
    base.write_text("def agent(obs, config=None):\n    return {'farmer': ['PASS'], 'hands': [], 'market': [['BUY_SEED', 'WHEAT', obs['step'] + 1]]}\n")
    missing = observation(day=2)
    missing['hour'] = 3
    none = copy.deepcopy(missing)
    none['step'] = None
    for obs in (missing, none):
        result = load_agent('clock::' + str(base))(obs, {'turnsPerDay': 24})
        assert result['market'][0][-1] == 52
