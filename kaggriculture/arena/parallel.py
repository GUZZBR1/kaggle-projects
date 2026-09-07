from concurrent.futures import ProcessPoolExecutor
import multiprocessing

from .match import run_match


def _run(kwargs):
    return run_match(**kwargs)


def matches(jobs, workers=4):
    if workers < 1:
        raise ValueError('workers must be positive')
    if workers == 1:
        for job in jobs:
            yield _run(job)
    else:
        with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context('spawn')) as pool:
            yield from pool.map(_run, jobs, chunksize=1)
