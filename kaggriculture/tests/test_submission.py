from pathlib import Path
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
