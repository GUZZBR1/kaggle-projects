"""Execution-continuity commitment bonus (issue #15, P2)."""
from agent.params import DEFAULTS
from agent.planner import policy
from arena.engine import make_environment
from arena.match import observations

IDLE = {'farmer': ['PASS'], 'hands': [], 'market': []}
MOVES = {'NORTH', 'SOUTH', 'EAST', 'WEST'}


def walk_share(seed, parameters):
    """Fraction of unit actions spent moving rather than acting on a tile."""
    env = make_environment(seed)
    moves = total = 0
    while not env.done:
        action = policy(observations(env.state)[0], dict(env.configuration), parameters)
        for unit in (action['farmer'], *action['hands']):
            total += 1
            moves += unit[0] in MOVES
        env.step([action, IDLE])
    return moves / total


def test_default_is_inert():
    """The shipped default must reproduce the pre-change policy exactly."""
    assert DEFAULTS['continuity_completion'] == 1.0
    env = make_environment(7)
    while not env.done:
        obs, cfg = observations(env.state)[0], dict(env.configuration)
        action = policy(obs, cfg)
        assert action == policy(obs, cfg, {'continuity_completion': 1.0})
        env.step([action, IDLE])


def test_bonus_keeps_units_on_the_job_underfoot():
    """A unit standing on a pending job should walk away less often."""
    assert walk_share(7, {'continuity_completion': 3.0}) < walk_share(7, {'continuity_completion': 1.0})
