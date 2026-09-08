"""The pool has to be fast without giving up the thing it exists for.

One process per game is the only real defence against a third-party bundle that mutates
something the arena reads, so a change that speeds the pool up must not buy the speed by
reusing a worker. And it must not change a single result: an evaluation harness whose
numbers depend on how it was scheduled cannot be used to decide anything.
"""
import multiprocessing

import pytest

from arena.parallel import PRELOAD, matches, start_method


JOB = dict(candidate='clock::versions/v004/main.py',
           opponent='clock::opponents/public/thomas_t95/main.py', backend='fast')


def test_the_start_method_prefers_forkserver_and_never_plain_fork():
    """A bare fork would inherit whatever the previous game's bundle left behind."""
    available = multiprocessing.get_all_start_methods()
    expected = 'forkserver' if 'forkserver' in available else 'spawn'
    assert start_method() == expected
    with pytest.raises(ValueError, match='Unusable start method'):
        start_method('fork')
    with pytest.raises(ValueError, match='Unusable start method'):
        start_method('not_a_method')


def test_an_explicit_method_is_honoured():
    assert start_method('spawn') == 'spawn'


def test_the_preload_list_is_importable_and_side_effect_free():
    """Anything preloaded is imported once in the forkserver parent and shared by every
    worker, so an import with side effects would leak across games."""
    import importlib
    for name in PRELOAD:
        importlib.import_module(name)


def test_workers_must_be_positive():
    with pytest.raises(ValueError, match='workers must be positive'):
        list(matches([], 0))


@pytest.mark.parametrize('workers', [1, 3])
def test_results_do_not_depend_on_the_start_method_or_the_worker_count(workers):
    """The whole harness rests on this: scheduling must be invisible in the numbers."""
    jobs = [dict(JOB, seed=1900 + index, seat=index % 2) for index in range(4)]
    reference = [(row['score'], row['money'], row['opponent_money'])
                 for row in matches(jobs, 1, method='spawn')]
    for method in ({'forkserver', 'spawn'} & set(multiprocessing.get_all_start_methods())):
        rows = list(matches(jobs, workers, method=method))
        assert [(r['score'], r['money'], r['opponent_money']) for r in rows] == reference, method


def test_every_job_is_played_exactly_once_and_in_order():
    jobs = [dict(JOB, seed=1910 + index, seat=0) for index in range(3)]
    rows = list(matches(jobs, 2))
    assert [row['seed'] for row in rows] == [1910, 1911, 1912]
