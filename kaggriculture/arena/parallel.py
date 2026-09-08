"""Run independent matches in parallel, one fresh process per game.

Isolation here is not a nicety. A submission bundle is third-party code that runs
`import`-time statements inside our interpreter, and `arena.agents` can *notice* a load
that rebinds something the arena reads but cannot undo it. The undo is the process
boundary, so every game gets its own address space and no worker is ever reused for a
second game.

That guarantee used to be paid for with a full interpreter start per game: `spawn` gives
the child nothing, so each of the 719-turn games re-imported the engine before playing.
Measured on 24 games, that overhead was about 1.15 of every 1.85 seconds — roughly
two thirds of the cost was not simulation.

`forkserver` keeps the guarantee and drops the overhead. A separate server process imports
the engine once and every worker is forked from it, so a worker starts warm but still
starts *clean*: the server never runs a game, so nothing a bundle did can reach the next
fork. Measured on the same 24 games, byte-identical final money in every configuration:

    method       1 worker              14 workers
    spawn        1.857 s/game          0.265 s/game   ( 3.8 games/s)
    forkserver   0.705 s/game          0.086 s/game   (11.6 games/s)

`forkserver` is POSIX-only, so the start method falls back to `spawn` where it is missing
and the results are the same either way.
"""
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import os

from .match import run_match

# Imported once in the forkserver parent, before any game exists. Keep this list to modules
# that are pure to import: anything with import-time side effects would have those effects
# shared by every forked worker instead of being redone per game.
PRELOAD = ('arena.match', 'arena.engine', 'arena.agents', 'arena.telemetry',
           'kaggle_environments')


def _run(kwargs):
    return run_match(**kwargs)


def start_method(requested=None):
    """`forkserver` when the platform has it, else `spawn`; never a bare `fork`.

    A bare `fork` would be faster still and is rejected on purpose: it is incompatible with
    one-process-per-game in `ProcessPoolExecutor`, and forking a process that has already
    played a game would hand the next game whatever the last bundle left behind.
    """
    requested = requested or os.environ.get('ARENA_START_METHOD')
    available = multiprocessing.get_all_start_methods()
    if requested:
        if requested not in available or requested == 'fork':
            raise ValueError(f'Unusable start method {requested!r}; available: {available}')
        return requested
    return 'forkserver' if 'forkserver' in available else 'spawn'


def matches(jobs, workers=4, method=None):
    if workers < 1:
        raise ValueError('workers must be positive')
    chosen = start_method(method)
    context = multiprocessing.get_context(chosen)
    if chosen == 'forkserver':
        context.set_forkserver_preload(list(PRELOAD))
    # max_tasks_per_child=1 is the isolation: a worker plays one game and exits.
    with ProcessPoolExecutor(max_workers=workers, mp_context=context,
                             max_tasks_per_child=1) as pool:
        yield from pool.map(_run, jobs, chunksize=1)
