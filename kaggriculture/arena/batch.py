"""The batch is the unit of distribution; the match stays the unit of isolation.

Ray reuses its worker processes between tasks, so one match per Ray task would quietly
undo the guarantee `arena/parallel.py` exists to provide: a third-party bundle runs code at
import time, `arena/agents.py` can notice a rebind but not undo it, and the undo is the
process boundary. `@ray.remote(max_calls=1)` would restore isolation by killing the worker
every task, but Ray's worker startup is heavier than the `spawn` we just removed, so it
would be slower than doing nothing.

So Ray -- when a second machine exists -- distributes **batches**, and inside each batch
the local forkserver pool still gives every game its own process. This module is that
batch layer, and it runs today on one machine with no Ray installed. The only seam a
transport has to replace is `map_batches`, which is why it is an argument rather than an
import.

Nothing here weakens the deadline. The barrier from issue #44 lives in the parent of each
match, so it holds one level down: `run_batch` called from a worker, a thread, or a Ray
task still kills a game that will not end. That matters because `signal.setitimer` only
works on the main thread of a POSIX process, and a driver running off the main thread would
silently degrade the in-process timer to the measure-afterwards fallback. Each match runs
in the main thread of its own child, so the timer is armed where it works, and the kill does
not depend on it either way.
"""
import os
import time

from .parallel import matches

# One or two cores left to the machine by default: an evaluation run that makes the host
# unusable gets interrupted by a human, and an interrupted run is worse than a slower one.
LEAVE_FREE = 1
BATCH_SIZE = 32


def worker_budget(cpus_free=LEAVE_FREE, cpus=None):
    """Workers to use on this host, never fewer than one."""
    if cpus_free < 0:
        raise ValueError('cpus_free cannot be negative')
    if cpus is None:
        cpus = len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else os.cpu_count()
    return max(1, (cpus or 1) - cpus_free)


def partition(jobs, size=BATCH_SIZE):
    """Contiguous batches, small enough that the slowest one cannot stall the queue.

    Small batches are what keeps a dynamic queue balanced without pre-splitting the work per
    machine, which is the failure mode of a static partition: the fast node idles while the
    slow one finishes its half.
    """
    jobs = list(jobs)
    if size < 1:
        raise ValueError('batch size must be positive')
    return [jobs[start:start + size] for start in range(0, len(jobs), size)]


def run_batch(specs, workers=4, method=None, timeout=-1):
    """Play one batch here, in job order. This is the body a Ray task would wrap."""
    started = time.monotonic()
    rows = list(matches(specs, workers=workers, method=method, timeout=timeout))
    return {'rows': rows, 'host': os.uname().nodename if hasattr(os, 'uname') else '',
            'pid': os.getpid(), 'wall_seconds': time.monotonic() - started,
            'games': len(rows)}


def _local(batches, workers, method, timeout):
    """Run batches one after another on this host. The default transport."""
    for specs in batches:
        yield run_batch(specs, workers=workers, method=method, timeout=timeout)


def batched_runner(size=BATCH_SIZE, method=None, timeout=-1, map_batches=None, on_batch=None):
    """A `runner(jobs, workers)` for `arena.jobs.execute`, with batching in the middle.

    `map_batches(batches, workers)` yields one envelope per batch, in batch order. The
    default runs them here; a Ray transport replaces exactly this function and nothing else.
    Rows are yielded in job order so `execute` -- and every caller that pairs jobs with rows
    positionally -- keeps working unchanged.
    """
    def runner(jobs, workers):
        batches = partition(jobs, size)
        transport = map_batches or (lambda parts, count: _local(parts, count, method, timeout))
        produced = 0
        for envelope in transport(batches, workers):
            rows = envelope['rows'] if isinstance(envelope, dict) else envelope
            if on_batch:
                on_batch(envelope)
            for row in rows:
                produced += 1
                yield row
        if produced != len(jobs):
            raise ValueError(f'Batches returned {produced} rows for {len(jobs)} jobs')
    return runner
