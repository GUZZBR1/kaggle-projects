"""Issue #23: prove whether agent state survives between games in a worker.

The sentinel deliberately leaks: it registers a helper module in `sys.modules`
and counts how many times it has been loaded into the same interpreter. If the
arena boundary holds, every load reports a count of zero. The control exercises
the same sentinel without the boundary, so a green suite is evidence about the
arena rather than evidence that the sentinel cannot detect anything.
"""
import os
import sys

import pytest

from arena.agents import load_agent, module_fingerprint, tampering
from arena.parallel import matches

# The log path is baked into the source rather than read from the environment. A worker
# forked from the forkserver inherits the environment the *server* started with, so an env
# var set after some other test warmed the pool never reaches the child, and which test
# warmed it first is alphabetical accident.
SENTINEL = '''
import os
import sys
import types

LOG = __SENTINEL_LOG__

helper = sys.modules.get('kagg_sentinel_helper')
leaked = helper is not None
if helper is None:
    helper = types.ModuleType('kagg_sentinel_helper')
    helper.loads = 0
    sys.modules['kagg_sentinel_helper'] = helper
seen = helper.loads
helper.loads += 1
GLOBAL_LOADS = globals().get('GLOBAL_LOADS', 0) + 1

with open(LOG, 'a') as stream:
    stream.write('%d %d %d %d\\n' % (os.getpid(), int(leaked), seen, GLOBAL_LOADS))


def agent(observation, configuration=None):
    return {'farmer': ['PASS'], 'hands': [], 'market': []}
'''


@pytest.fixture
def sentinel(tmp_path):
    path = tmp_path / 'sentinel.py'
    log = tmp_path / 'loads.log'
    log.write_text('')
    path.write_text(SENTINEL.replace('__SENTINEL_LOG__', repr(str(log))))

    def records():
        return [tuple(int(field) for field in line.split())
                for line in log.read_text().splitlines()]
    return str(path), records


def test_the_sentinel_detects_leakage_when_the_boundary_is_removed(sentinel):
    # Control: without the arena's unwinding, the second load sees the first.
    path, records = sentinel
    source = compile(open(path).read(), path, 'exec')
    try:
        for _ in range(2):
            exec(source, {'__name__': 'control'})
    finally:
        sys.modules.pop('kagg_sentinel_helper', None)
    assert [(leaked, seen) for _, leaked, seen, _ in records()] == [(0, 0), (1, 1)]


def test_repeated_loads_in_one_interpreter_do_not_leak(sentinel):
    path, records = sentinel
    for _ in range(3):
        load_agent(path)
    assert 'kagg_sentinel_helper' not in sys.modules
    assert '__kaggriculture_submission__' not in sys.modules
    assert all((leaked, seen, module_loads) == (0, 0, 1)
               for _, leaked, seen, module_loads in records())


def test_a_failing_load_still_unwinds_the_modules(tmp_path):
    broken = tmp_path / 'broken.py'
    broken.write_text("import types, sys\n"
                      "sys.modules['kagg_broken_helper'] = types.ModuleType('kagg_broken_helper')\n"
                      "raise RuntimeError('bundle exploded')\n")
    with pytest.raises(RuntimeError):
        load_agent(str(broken))
    assert 'kagg_broken_helper' not in sys.modules
    assert '__kaggriculture_submission__' not in sys.modules


def bundle(tmp_path, name, body):
    path = tmp_path / (name + '.py')
    path.write_text(body + "\ndef agent(observation, configuration=None):\n"
                           "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")
    return str(path)


def test_mutating_an_already_imported_module_is_refused_not_absorbed(tmp_path):
    """The hole the unwinding cannot close is now refused at the door.

    `load_agent` can drop the modules a bundle registered, but it cannot undo a
    bundle that reaches into a module the arena already imported. Nothing at
    load time can. So the load fingerprints arena-visible state and refuses a
    bundle that changed it, and the isolation itself still comes from running
    one process per game.
    """
    import json
    original = json.dumps
    try:
        with pytest.raises(RuntimeError, match='json.dumps rebound'):
            load_agent(bundle(tmp_path, 'hijack', "import json\njson.dumps = lambda *a, **k: 'x'"))
    finally:
        json.dumps = original
    assert json.dumps({'a': 1}) == '{"a": 1}'


def test_patching_the_interpreter_is_detected_whoever_imported_it_first(tmp_path):
    # Detection must not depend on the arena having imported the interpreter
    # first, so the fingerprint imports it itself when a caller has not.
    from arena.engine import official
    module = official()
    original = module.market_price
    try:
        with pytest.raises(RuntimeError, match='market_price rebound'):
            load_agent(bundle(tmp_path, 'repriced',
                              "from kaggle_environments.envs.kaggriculture import kaggriculture as k\n"
                              "k.market_price = lambda *a: 9999"))
    finally:
        module.market_price = original


@pytest.mark.parametrize('body,expected', [
    ("import builtins\nbuiltins.PWNED = 1", 'PWNED added'),
    ("import random\nrandom.seed(1)", '__random_state__'),
    ("import copy\ncopy.deepcopy = lambda x: x", 'copy.deepcopy rebound'),
])
def test_the_fingerprint_covers_the_state_a_game_depends_on(tmp_path, body, expected):
    import builtins
    import copy as copy_module
    import random as random_module
    saved = (copy_module.deepcopy, random_module.getstate())
    try:
        with pytest.raises(RuntimeError, match=expected):
            load_agent(bundle(tmp_path, 'mutate', body))
    finally:
        builtins.__dict__.pop('PWNED', None)
        copy_module.deepcopy, _ = saved
        random_module.setstate(saved[1])


def test_registering_a_private_helper_module_is_not_tampering(tmp_path):
    # The boundary must not cry wolf: bundles legitimately build helper modules.
    load_agent(bundle(tmp_path, 'helper',
                      "import sys, types\n"
                      "m = types.ModuleType('kagg_private_helper')\nm.x = 1\n"
                      "sys.modules['kagg_private_helper'] = m"))
    assert load_agent.last_tampering == []
    assert 'kagg_private_helper' not in sys.modules


@pytest.mark.parametrize('name', ['opponents/public/cok_v10/main.py', 'opponents/frozen/crop/main.py',
                                  'opponents/frozen/animal/main.py', 'versions/v000/main.py',
                                  'versions/v002/main.py', 'champion', 'liquidity_first'])
def test_every_bundle_the_project_actually_runs_loads_clean(name):
    load_agent(name)
    assert load_agent.last_tampering == []


def test_a_bundle_importing_a_native_library_does_not_crash_the_worker(tmp_path):
    """Unwinding must never drop a module the arena itself imported.

    Deleting a native extension from sys.modules and re-importing it later
    terminates the process, so `before` is captured after the fingerprint has
    finished importing anything it needs.
    """
    load_agent(bundle(tmp_path, 'native', 'import kaggle_environments'))
    assert load_agent.last_tampering == []
    assert 'kaggle_environments' in sys.modules


def test_workers_are_never_reused_between_games(sentinel):
    path, records = sentinel
    jobs = [dict(candidate=path, opponent='pass', seed=seed, seat=seat,
                 telemetry_enabled=False)
            for seed in (5, 6) for seat in (0, 1)]
    rows = list(matches(jobs, workers=2))
    assert len(rows) == 4 and not any(row['failures'] for row in rows)
    loads = records()
    # A→B→A ordering shares the pool, so a reused interpreter would show a
    # second load with a nonzero count. One fresh process per game means the
    # sentinel is always the first thing loaded in its own interpreter.
    assert len(loads) == 4
    assert len({pid for pid, _, _, _ in loads}) == 4
    assert all((leaked, seen, module_loads) == (0, 0, 1)
               for _, leaked, seen, module_loads in loads)
    assert os.getpid() not in {pid for pid, _, _, _ in loads}
