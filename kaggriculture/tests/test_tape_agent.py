"""A tape agent is the honest floor: fixed behaviour, no adaptation at all."""
import json

import pytest

from arena.agents import load_agent
from experiments.tape_agent import build, select


def stream(n=719):
    return [{'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW']],
             'market': [['SELL', 'WHEAT', 3], ['PASS'], ['SELL', 'MELON', 0]]} for _ in range(n)]


def test_a_tape_must_cover_the_whole_season(tmp_path):
    with pytest.raises(ValueError, match='719'):
        build(stream(100), tmp_path / 'short.py')


def test_the_generated_agent_replays_the_tape_by_the_canonical_clock(tmp_path):
    actions = stream()
    actions[5] = {'farmer': ['HARVEST'], 'hands': [], 'market': []}
    path = build(actions, tmp_path / 'tape.py', provenance='unit test')
    agent = load_agent(str(path))

    for turn in (0, 5, 718):
        result = agent({'step': turn, 'day': turn // 24, 'hour': turn % 24}, None)
        assert result['farmer'] == actions[turn]['farmer']
    # The clock is derived when the engine omits step, exactly as the arena does.
    assert agent({'day': 0, 'hour': 5}, None)['farmer'] == ['HARVEST']


def test_out_of_range_turns_fall_back_to_pass(tmp_path):
    agent = load_agent(str(build(stream(), tmp_path / 'tape.py')))
    for turn in (-1, 719, 5000):
        assert agent({'step': turn}, None) == {'farmer': ['PASS'], 'hands': [], 'market': []}


def test_unparseable_market_slots_become_a_harmless_placeholder(tmp_path):
    """Slots race by index, so a bad slot must not shift the ones after it."""
    agent = load_agent(str(build(stream(), tmp_path / 'tape.py')))
    market = agent({'step': 0}, None)['market']
    assert market[0] == ['SELL', 'WHEAT', 3]
    assert market[1] == ['SELL', 'WHEAT', 0], "['PASS'] is replaced, not dropped"
    assert market[2] == ['SELL', 'WHEAT', 0], 'a zero-quantity sale stays a placeholder'
    assert len(market) == 3, 'slot count is preserved'


def test_the_agent_never_hands_out_its_own_tape_objects(tmp_path):
    agent = load_agent(str(build(stream(), tmp_path / 'tape.py')))
    first = agent({'step': 0}, None)
    first['farmer'].append('MUTATED')
    first['market'].clear()
    assert agent({'step': 0}, None)['farmer'] == ['NORTH']
    assert len(agent({'step': 0}, None)['market']) == 3


def test_the_market_is_capped_at_ten_slots(tmp_path):
    actions = stream()
    actions[0] = {'farmer': ['PASS'], 'hands': [], 'market': [['HIRE']] * 14}
    agent = load_agent(str(build(actions, tmp_path / 'tape.py')))
    assert len(agent({'step': 0}, None)['market']) == 10


def test_select_reports_an_empty_or_out_of_range_library():
    with pytest.raises(ValueError, match='empty'):
        select({'tapes': []})
    with pytest.raises(ValueError, match='outside a library'):
        select({'tapes': [{'id': 'a'}]}, rank=7)
    assert select({'tapes': [{'id': 'a'}, {'id': 'b'}]}, rank=1)['id'] == 'b'
