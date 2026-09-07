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

from arena.agents import load_agent
from arena.parallel import matches

SENTINEL = '''
import os
import sys
import types

helper = sys.modules.get('kagg_sentinel_helper')
leaked = helper is not None
if helper is None:
    helper = types.ModuleType('kagg_sentinel_helper')
    helper.loads = 0
    sys.modules['kagg_sentinel_helper'] = helper
seen = helper.loads
helper.loads += 1
GLOBAL_LOADS = globals().get('GLOBAL_LOADS', 0) + 1

with open(os.environ['KAGG_SENTINEL_LOG'], 'a') as stream:
    stream.write('%d %d %d %d\\n' % (os.getpid(), int(leaked), seen, GLOBAL_LOADS))


def agent(observation, configuration=None):
    return {'farmer': ['PASS'], 'hands': [], 'market': []}
'''


@pytest.fixture
def sentinel(tmp_path, monkeypatch):
    path = tmp_path / 'sentinel.py'
    path.write_text(SENTINEL)
    log = tmp_path / 'loads.log'
    log.write_text('')
    monkeypatch.setenv('KAGG_SENTINEL_LOG', str(log))

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


def test_mutating_an_already_imported_module_does_leak_in_process(tmp_path):
    """The boundary has a real hole, and this is why the pool never reuses a worker.

    `load_agent` unwinds `sys.modules`, but it cannot undo a bundle that
    reaches into a module the arena itself already imported. Nothing at load
    time can, so the isolation has to come from the process, not the namespace.
    """
    import json
    hijack = tmp_path / 'hijack.py'
    hijack.write_text("import json\n"
                      "json.dumps = lambda *a, **k: 'hijacked'\n"
                      "def agent(observation, configuration=None):\n"
                      "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")
    original = json.dumps
    try:
        load_agent(str(hijack))
        assert json.dumps({'a': 1}) == 'hijacked'
    finally:
        json.dumps = original
    assert json.dumps({'a': 1}) == '{"a": 1}'


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
