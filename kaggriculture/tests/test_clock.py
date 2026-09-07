"""Issue #20: the canonical clock is day/hour, never a trusted `step` key."""
import copy

import pytest

from agent.planner import policy
from agent.state import State
from arena.engine import make_environment
from arena.match import observations, run_match


def clock(step, day=3, hour=7, turns=24):
    obs = {'day': day, 'hour': hour}
    if step is not ...:
        obs['step'] = step
    return State(obs, {'turnsPerDay': turns})


def test_omitted_and_explicit_none_both_derive_the_canonical_step():
    assert clock(...).step == 3 * 24 + 7
    assert clock(None).step == 3 * 24 + 7
    assert clock(3 * 24 + 7).step == 3 * 24 + 7


def test_step_disagreeing_with_the_clock_is_rejected_instead_of_masked():
    for supplied in (0, 5, 3 * 24 + 6, 3 * 24 + 8, True, 79.0, '79'):
        with pytest.raises(ValueError):
            clock(supplied).step


@pytest.mark.parametrize('day,hour,turns', [(-1, 0, 24), (0, 24, 24), (0, -1, 24), (0, 0, 0),
                                            (None, 0, 24), (0, None, 24), (1.0, 0, 24), (True, 0, 24)])
def test_malformed_clocks_fail_closed(day, hour, turns):
    with pytest.raises(ValueError):
        clock(..., day, hour, turns).step


def test_turns_left_follows_the_derived_step():
    state = State({'day': 29, 'hour': 23}, {'turnsPerDay': 24, 'episodeSteps': 720})
    assert state.step == 719
    assert state.turns_left == 0


@pytest.mark.parametrize('seat', [0, 1])
def test_arena_never_lends_seat_one_a_step_it_would_not_receive(seat):
    # Upstream ships `step` to seat 0 only. Mirroring it would hide a submission
    # that reads the private key and passes in the lab but fails on Kaggle.
    obs = observations(make_environment(11).state)
    assert 'step' in obs[0] and 'step' not in obs[1]
    assert obs[seat]['day'] == 0 and obs[seat]['hour'] == 0


@pytest.mark.parametrize('mutate', [lambda o: o.pop('step', None), lambda o: o.update(step=None)])
@pytest.mark.parametrize('seat', [0, 1])
def test_policy_is_indifferent_to_the_step_key(mutate, seat):
    env = make_environment(23)
    for _ in range(40):
        env.step([{'farmer': ['PASS'], 'hands': [], 'market': []}] * 2)
    obs = observations(env.state)[seat]
    obs['player'] = seat
    reference = policy(copy.deepcopy(obs), env.configuration, {})
    stripped = copy.deepcopy(obs)
    mutate(stripped)
    assert policy(stripped, env.configuration, {}) == reference


@pytest.mark.parametrize('seat', [0, 1])
def test_fast_and_official_agree_on_the_clock(seat):
    fast = run_match('challenger', 'starter', 31, seat)
    official = run_match('challenger', 'starter', 31, seat, backend='official')
    assert fast['steps'] == official['steps'] == 719
    assert not fast['failures'] and not official['failures']
    assert [d['day'] for d in fast['daily']] == [d['day'] for d in official['daily']]
    assert sum(d['turns'] for d in fast['daily']) == 719
