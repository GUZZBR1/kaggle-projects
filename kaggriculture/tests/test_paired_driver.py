import json

import pytest

from arena import league, paired
from arena.agents import agent_hash
from arena.seeds import load_registry


@pytest.fixture
def registry(tmp_path):
    path = tmp_path / 'seeds.json'
    path.write_text(json.dumps(dict(schema_version=1, revision=1, holdout_start=9000000,
        history=[], entries=[
            dict(id='dev', start=1000, end=1100, classification='dev', provenance=['test']),
            dict(id='validation', start=100100, end=100200, classification='validation', provenance=['test']),
            dict(id='holdout', start=9000000, end=None, classification='holdout', provenance=['test'])])))
    return path


@pytest.fixture
def fake_engine(monkeypatch, registry):
    calls = []
    monkeypatch.setattr(paired, 'fingerprint', lambda: {})
    def matches(jobs, workers):
        calls.append(jobs)
        for job in jobs:
            if job['seed'] >= 100100:
                state, _ = load_registry(registry)
                assert state['revision'] == 2, 'both legs share one consumption'
                assert len(state['history'][0]['run']['batch_members']) == 2
            yield dict(job, candidate_hash=agent_hash(job['candidate']),
                opponent_hash=agent_hash(job['opponent']), environment={},
                configuration={'seed': job['seed']}, score=.5, margin=0,
                money=100, opponent_money=100, failures=[], opponent_failures=[],
                unsold_items=0, runtime_ms=[1], audit={}, sales={}, steps=719, wall_seconds=.01)
    monkeypatch.setattr(league, 'matches', matches)
    return calls


def run(tmp_path, registry, **kwargs):
    return paired.run_pair('pass', 'starter', ['random'], range(100100, 100200),
                           tmp_path / 'run', registry_path=registry, split='validation', **kwargs)


def test_both_100_block_legs_share_one_admission_and_emit_evidence(tmp_path, registry, fake_engine):
    result, gate = run(tmp_path, registry)
    state, _ = load_registry(registry)
    assert len(fake_engine) == 2
    assert len(fake_engine[0]) == len(fake_engine[1]) == 200
    assert state['revision'] == 2 and len(state['history']) == 1
    assert result['seed_blocks'] == 100
    assert gate['verdict'] == 'NO SUBMIT'
    assert result['snapshot']['ratings_sha256']
    for name in ('plan.json', 'comparison.json', 'gate.json', 'report.md',
                 'baseline/matches.jsonl', 'candidate/matches.jsonl'):
        assert (tmp_path / 'run' / name).is_file()


@pytest.mark.parametrize('problem', ['used_output', 'insufficient_seeds', 'invalid_agent', 'holdout'])
def test_prechecks_do_not_consume_seeds(tmp_path, registry, fake_engine, problem):
    before = registry.read_bytes()
    args = dict(baseline='pass', candidate='starter', opponents=['random'],
                seeds=list(range(100100, 100200)), output=tmp_path / 'run',
                split='validation', registry_path=registry)
    if problem == 'used_output':
        args['output'].mkdir()
    elif problem == 'insufficient_seeds':
        args['seeds'] = args['seeds'][:75]
    elif problem == 'invalid_agent':
        args['candidate'] = 'missing.py'
    else:
        args['seeds'] = list(range(9000000, 9000100))
    with pytest.raises((ValueError, FileExistsError)):
        paired.run_pair(**args)
    assert registry.read_bytes() == before
    assert not fake_engine


def test_partial_run_keeps_validation_burned_and_emits_no_verdict(tmp_path, registry, fake_engine, monkeypatch):
    original = league.matches
    def interrupted(jobs, workers):
        yield next(iter(original(jobs, workers)))
        raise RuntimeError('worker interrupted')
    monkeypatch.setattr(league, 'matches', interrupted)
    with pytest.raises(RuntimeError, match='interrupted'):
        run(tmp_path, registry)
    assert load_registry(registry)[0]['revision'] == 2
    assert (tmp_path / 'run/failure.json').is_file()
    assert not (tmp_path / 'run/gate.json').exists()


def test_artifact_drift_is_detected_before_second_leg(tmp_path, registry, fake_engine, monkeypatch):
    original = paired.check_spec
    def check(spec):
        return 'changed' if fake_engine and spec == 'starter' else original(spec)
    monkeypatch.setattr(paired, 'check_spec', check)
    with pytest.raises(ValueError, match='changed after'):
        run(tmp_path, registry)
    assert len(fake_engine) == 1
    assert not (tmp_path / 'run/gate.json').exists()


def test_strong_only_uses_frozen_ratings_and_rejects_empty_panel(tmp_path, registry, fake_engine):
    with pytest.raises(ValueError, match='No current strong'):
        run(tmp_path, registry, strong_only=True, ratings={})
    assert not fake_engine
    rating = dict(rating=2500, observed_at=paired.date.today().isoformat(), kind='direct')
    result, _ = run(tmp_path, registry, strong_only=True, ratings={'random': rating})
    assert result['strong']['games'] == 200
    assert result['execution']['strong_only'] is True
