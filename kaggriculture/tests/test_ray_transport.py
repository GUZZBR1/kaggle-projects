from types import SimpleNamespace

import pytest

from arena.batch import make_batch
from arena.ray_transport import RayBatchMapper


class RayError(Exception):
    pass


class RayTaskError(RayError):
    def __init__(self, cause):
        self.cause = cause

    def as_instanceof_cause(self):
        return self.cause


class Ref:
    def __init__(self, value=None, error=None):
        self.value, self.error = value, error


class Remote:
    def __init__(self, function, ray, options):
        self.function, self.ray, self.options_seen = function, ray, options

    def options(self, **options):
        return Remote(self.function, self.ray, {**self.options_seen, **options})

    def remote(self, *args):
        try:
            return Ref(value=self.function(*args))
        except Exception as exc:
            return Ref(error=RayTaskError(exc))


class FakeRay:
    exceptions = SimpleNamespace(RayError=RayError, RayTaskError=RayTaskError)
    util = SimpleNamespace(scheduling_strategies=SimpleNamespace(
        NodeAffinitySchedulingStrategy=lambda node_id, soft: (node_id, soft)))

    def __init__(self):
        self.remote_options = []

    def cluster_resources(self):
        return {'CPU': 4}

    def nodes(self):
        return [{'Alive': True, 'NodeID': 'node-a'}]

    def remote(self, **options):
        self.remote_options.append(options)
        return lambda function: Remote(function, self, options)

    def get(self, value):
        if isinstance(value, list):
            return [self.get(item) for item in value]
        if value.error:
            raise value.error
        return value.value

    def wait(self, refs, num_returns=1):
        return refs[:num_returns], refs[num_returns:]


class SequenceTask:
    def __init__(self, refs):
        self.refs = iter(refs)
        self.calls = 0

    def remote(self, *args):
        self.calls += 1
        return next(self.refs)


def test_mapper_disables_ray_retries_and_counts_cluster_slots():
    ray = FakeRay()
    mapper = RayBatchMapper(ray, cpus_per_worker=2)
    assert mapper.available_slots == 2
    assert ray.remote_options == [
        {'num_cpus': 2, 'max_retries': 0, 'retry_exceptions': False},
        {'num_cpus': 0, 'max_retries': 0, 'retry_exceptions': False},
    ]


def test_mapper_retries_a_system_failure_but_not_application_failure(monkeypatch):
    batch = make_batch([{'candidate': 'pass', 'opponent': 'pass', 'seed': 1,
                         'seat': 0, 'backend': 'fast'}])
    result = {'batch_id': batch['batch_id']}
    ray = FakeRay()
    mapper = RayBatchMapper(ray, attempts=2)
    monkeypatch.setattr(mapper, 'verify_cluster', lambda batches: [])
    task = SequenceTask([Ref(error=RayError('node died')), Ref(value=result)])
    mapper._task = task
    assert list(mapper([batch], 1)) == [result]
    assert task.calls == 2

    mapper._task = SequenceTask([Ref(error=RayTaskError(ValueError('bad batch')))])
    with pytest.raises(ValueError, match='bad batch'):
        list(mapper([batch], 1))
    assert mapper._task.calls == 1
