from pathlib import Path
import pytest
import tarfile

from arena.agents import load_agent, invoke
from arena.engine import make_environment
from arena.match import observations
from submission.build import build
from submission.preflight import preflight


def test_standalone_matches_policy_and_runs_real_loader(tmp_path):
    path = tmp_path / 'main.py'
    manifest = build(path)
    function = load_agent(str(path))
    builtin = load_agent('challenger')
    env = make_environment(13)
    while not env.done:
        obs = observations(env.state)
        a = invoke(function, obs[0], dict(env.configuration))
        assert a == invoke(builtin, obs[0], dict(env.configuration))
        env.step([a, {'farmer': ['PASS'], 'market': []}])
    with tarfile.open(path.with_suffix('.tar.gz')) as archive:
        assert archive.getnames() == ['main.py']
    assert preflight(path)['status'] == 'PASSED'
    assert manifest['sha256'] == build(path)['sha256']


def _artifact(tmp_path, name, body):
    path = tmp_path / (name + '.py')
    path.write_text(body)
    return str(path)


ALIVE = ("def agent(observation, configuration=None):\n"
         "    return {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE']]}\n")

# The v47 failure mode the community lost submissions to: the policy raises, the
# artifact catches it and returns PASS, and every structural check still passes.
SILENT = ("def _policy(observation):\n"
          "    raise RuntimeError('a child controller blows up')\n\n"
          "def agent(observation, configuration=None):\n"
          "    try:\n"
          "        return _policy(observation)\n"
          "    except Exception:\n"
          "        return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")


def test_liveness_reads_what_the_artifact_actually_did():
    from submission.preflight import liveness
    steps = [None] + [[{'action': {'farmer': ['PASS'], 'hands': [], 'market': []}}] for _ in range(3)]
    steps += [[{'action': {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW']],
                           'market': [['HIRE']]}}] for _ in range(2)]
    report = liveness(steps, 0)
    assert report['turns'] == 5
    assert report['first_acting_turn'] == 3
    assert report['farmer_actions'] == 2 and report['hand_actions'] == 2
    assert report['market_orders'] == 2
    assert report['longest_idle_streak'] == 3


def test_a_pass_only_artifact_is_refused(tmp_path):
    from submission.preflight import preflight
    body = "def agent(observation, configuration=None):\n    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n"
    with pytest.raises(RuntimeError, match='PASS-only artifact'):
        preflight(_artifact(tmp_path, 'passonly', body))


def test_a_silent_pass_fallback_is_refused(tmp_path):
    """This is the case the old preflight could not see.

    The wrapper reports DONE, the episode reaches 720 states and no error is
    logged, because the artifact swallowed its own exception. Only looking at
    what it actually played reveals it.
    """
    from submission.preflight import preflight
    with pytest.raises(RuntimeError) as caught:
        preflight(_artifact(tmp_path, 'silent', SILENT))
    message = str(caught.value)
    assert 'liveness' in message
    assert 'starting capital' in message


def test_a_playing_artifact_passes_and_reports_its_activity(tmp_path):
    from submission.preflight import preflight
    result = preflight(_artifact(tmp_path, 'alive', ALIVE))
    assert result['status'] == 'PASSED'
    assert result['states'] == 720
    for report in result['liveness']:
        assert report['turns'] == 719
        assert report['first_acting_turn'] == 0
        assert report['market_orders'] == 719


def test_the_shipped_version_is_alive(tmp_path):
    from submission.preflight import preflight
    result = preflight('versions/v002/main.py')
    assert result['status'] == 'PASSED'
    for report in result['liveness']:
        assert report['farmer_action_rate'] > .5
        assert report['longest_idle_streak'] < 72
        assert report['distinct_farmer_actions'] > 3
