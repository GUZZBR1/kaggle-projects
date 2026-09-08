"""A bundle must not be able to outlive our deadline, and it could.

The per-turn timer is armed with `signal.setitimer` inside the interpreter that runs the
bundle, so the bundle can switch it off; a probe that did exactly that overran the deadline
by three seconds and the match recorded no failure at all. Worse, a bundle that never
returns hung the worker for good, with nothing to notice it. These tests hold the two
halves of the fix: the elapsed-time check that makes an overrun a failure, and the parent's
hard deadline that kills the process group of a game that will not end.
"""
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import pytest

from arena.agents import WATCHED, load_agent
from arena.match import run_match
from arena.parallel import matches, timeout_row


def bundle(tmp_path, name, body):
    path = tmp_path / f'{name}.py'
    path.write_text(body, encoding='utf-8')
    return str(path)


DISARMS_THE_TIMER = '''
import signal, time
_burnt = False

def agent(observation, configuration=None):
    global _burnt
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    signal.setitimer(signal.ITIMER_REAL, 0)
    if not _burnt:
        _burnt = True
        time.sleep(float(configuration["actTimeout"]) + .4)
    return {"farmer": ["PASS"], "hands": [], "market": []}
'''

# It disarms the timer first, which is the whole point: a bundle that leaves the timer
# armed is stopped by it, and this one is not.
HANGS_FOREVER = '''
import signal, time

def agent(observation, configuration=None):
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    signal.setitimer(signal.ITIMER_REAL, 0)
    while True:
        time.sleep(.05)
'''

HANGS_WITH_A_CHILD = '''
import signal, subprocess, sys, time
from pathlib import Path

def agent(observation, configuration=None):
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    signal.setitimer(signal.ITIMER_REAL, 0)
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)"])
    Path(r"{pidfile}").write_text(str(child.pid))
    while True:
        time.sleep(.05)
'''

REBINDS_SETITIMER = '''
import signal
signal.setitimer = lambda *args, **kwargs: None

def agent(observation, configuration=None):
    return {"farmer": ["PASS"], "hands": [], "market": []}
'''


def test_an_overrun_is_recorded_even_when_the_bundle_disarms_the_timer(tmp_path):
    """The probe from the issue: it used to burn the deadline with `failures: []`."""
    path = bundle(tmp_path, 'disarm', DISARMS_THE_TIMER)
    row = run_match(candidate=path, opponent='pass', seed=7, telemetry_enabled=False)
    assert row['failures'], 'an overrun with the timer disarmed must not go unrecorded'
    assert row['failures'][0]['kind'] == 'TimeoutError'
    assert 'did not fire' in row['failures'][0]['message']
    assert row['failures'][0]['step'] == 0


def test_an_honest_agent_is_not_accused_of_overrunning(tmp_path):
    """The check reads a clock, so it must not fire on an agent that simply plays."""
    row = run_match(candidate='pass', opponent='pass', seed=7, telemetry_enabled=False)
    assert row['failures'] == [] and row['opponent_failures'] == []


def test_a_hanging_bundle_is_killed_and_the_run_survives(tmp_path):
    """The mandatory test: a game that will not end must end anyway, within the limit."""
    jobs = [dict(candidate=bundle(tmp_path, 'hang', HANGS_FOREVER), opponent='pass',
                 seed=11, seat=0, telemetry_enabled=False),
            dict(candidate='pass', opponent='pass', seed=12, seat=0, telemetry_enabled=False)]
    started = time.monotonic()
    rows = list(matches(jobs, workers=2, timeout=4))
    elapsed = time.monotonic() - started
    assert elapsed < 40, f'the kill did not happen near the limit: {elapsed:.1f}s'
    killed, healthy = rows
    assert killed['timed_out'] is True
    assert killed['failures'] and killed['failures'][0]['kind'] == 'MatchTimeout'
    assert killed['opponent_failures'], 'a hang is not attributable, so both sides carry it'
    assert killed['score'] == .5
    assert killed['seed'] == 11 and healthy['seed'] == 12
    # The healthy job still played: one poisoned game must not poison the batch.
    assert healthy.get('timed_out') is None and healthy['steps'] > 0


@pytest.mark.skipif(not hasattr(os, 'killpg'), reason='needs POSIX process groups')
def test_the_kill_reaches_a_subprocess_the_bundle_started(tmp_path):
    """Killing only the child we know about would leave the bundle's own children running."""
    pidfile = tmp_path / 'child.pid'
    path = bundle(tmp_path, 'hangchild', HANGS_WITH_A_CHILD.format(pidfile=pidfile))
    rows = list(matches([dict(candidate=path, opponent='pass', seed=13, seat=0,
                              telemetry_enabled=False)], workers=1, timeout=5))
    assert rows[0]['timed_out'] is True
    assert pidfile.is_file(), 'the bundle never got far enough to start its child'
    grandchild = int(pidfile.read_text())
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            os.kill(grandchild, 0)
        except (ProcessLookupError, PermissionError):
            return
        time.sleep(.1)
    os.kill(grandchild, signal.SIGKILL)  # do not leave it behind for the next test
    pytest.fail('the subprocess the bundle started outlived the kill')


def test_the_timeout_row_carries_provenance_like_any_other(tmp_path):
    """Nothing downstream should have to special-case a killed game."""
    job = dict(candidate='pass', opponent='pass', seed=99, seat=1, backend='fast')
    row = timeout_row(job, 12.5)
    assert row['candidate_hash'] and row['opponent_hash']
    assert row['seed'] == 99 and row['seat'] == 1 and row['score'] == .5
    assert row['runtime_ms'] == [] and row['margin'] == 0.
    assert '12.5' in row['failures'][0]['message']


def test_the_barrier_can_be_disabled_but_not_set_to_nonsense():
    with pytest.raises(ValueError, match='timeout must be positive'):
        list(matches([], 1, timeout=0))
    with pytest.raises(ValueError, match='timeout must be positive'):
        list(matches([], 1, timeout=-5))
    assert list(matches([], 1, timeout=None)) == []


def test_signal_is_watched_and_a_bundle_reaching_for_the_timer_is_reported(tmp_path):
    """Watching `signal` does not protect the timer; it records who reached for it."""
    assert 'signal' in WATCHED
    load_agent(bundle(tmp_path, 'rebind', REBINDS_SETITIMER), strict=False)
    assert any('signal.setitimer' in finding for finding in load_agent.last_tampering)
