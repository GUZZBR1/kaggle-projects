"""Issue #21: the registry is the only authority on which seeds may be run."""
import json

import pytest

from arena.seeds import admit_run, load_registry, parse_seeds, validate_seeds


def write(path, entries, revision=1, holdout_start=9000000, schema=1):
    payload = {'schema_version': schema, 'revision': revision, 'holdout_start': holdout_start,
               'entries': entries, 'history': []}
    path.write_text(json.dumps(payload, indent=2) + '\n')
    return path


HOLDOUT = {'id': 'final-holdout', 'start': 9000000, 'end': None, 'classification': 'holdout',
           'provenance': ['reserved for the release decision']}


def registry(tmp_path, *entries, **kwargs):
    return write(tmp_path / 'registry.json', [*entries, dict(HOLDOUT)], **kwargs)


def entry(id, start, end, classification, provenance=('test',)):
    return {'id': id, 'start': start, 'end': end, 'classification': classification,
            'provenance': list(provenance)}


def test_the_shipped_registry_is_well_formed():
    data, digest = load_registry()
    assert data['schema_version'] == 1 and len(digest) == 64
    assert {e['classification'] for e in data['entries']} <= {'dev', 'seen', 'validation',
                                                              'diagnostic', 'holdout'}
    assert all(e['provenance'] for e in data['entries'])


def test_documented_history_keeps_its_classification():
    for seed, split in [(1000, 'dev'), (1099, 'dev'), (100000, 'seen'), (100099, 'seen'),
                        (100100, 'validation'), (314159, 'diagnostic')]:
        assert validate_seeds([seed], split)['split'] == split


def test_burned_evidence_cannot_be_relabelled_as_clean_validation():
    with pytest.raises(ValueError, match='is seen, not validation'):
        validate_seeds([100000], 'validation')


@pytest.mark.parametrize('split', ['dev', 'seen', 'validation', 'diagnostic'])
def test_the_holdout_is_rejected_for_every_ordinary_split(split):
    with pytest.raises(ValueError):
        validate_seeds([9000000], split)
    with pytest.raises(ValueError):
        validate_seeds([9999999], split)


def test_unregistered_seeds_fail_closed():
    with pytest.raises(ValueError, match='Unregistered seed'):
        validate_seeds([500000], 'dev')


def test_duplicates_and_bad_splits_are_refused():
    with pytest.raises(ValueError):
        validate_seeds([1000, 1000], 'dev')
    with pytest.raises(ValueError):
        validate_seeds([1000], 'holdout')
    with pytest.raises(ValueError):
        validate_seeds([], 'dev')
    with pytest.raises(ValueError):
        validate_seeds([-1], 'dev')


def test_parse_seeds_refuses_duplicate_or_negative_ranges():
    assert parse_seeds('1000:1003') == [1000, 1001, 1002]
    with pytest.raises(ValueError):
        parse_seeds('7,7')
    with pytest.raises(ValueError):
        parse_seeds('-3')


@pytest.mark.parametrize('entries', [
    [entry('a', 0, 100, 'dev'), entry('b', 50, 150, 'validation')],
    [entry('a', 0, 100, 'dev'), entry('a', 100, 200, 'validation')],
    [entry('a', 0, None, 'dev')],
    [entry('a', 100, 100, 'dev')],
    [entry('a', 0, 100, 'unknown')],
    [entry('a', 0, 100, 'dev', provenance=())],
])
def test_a_malformed_registry_is_never_loaded(tmp_path, entries):
    with pytest.raises(ValueError):
        load_registry(registry(tmp_path, *entries))


def test_the_holdout_boundary_cannot_be_moved(tmp_path):
    path = write(tmp_path / 'moved.json', [{**HOLDOUT, 'start': 8000000}], holdout_start=8000000)
    with pytest.raises(ValueError):
        load_registry(path)


def test_an_unsupported_schema_is_refused(tmp_path):
    with pytest.raises(ValueError):
        load_registry(registry(tmp_path, entry('a', 0, 100, 'dev'), schema=2))


def test_validation_seeds_are_burned_before_the_run(tmp_path):
    path = registry(tmp_path, entry('reserved', 0, 10, 'validation'))
    metadata = admit_run([2, 3], 'validation', {'candidate': 'challenger'}, path)
    assert metadata['consumption_revision'] == 2

    # The same seeds are now spent evidence, whatever the outcome of that run.
    with pytest.raises(ValueError, match='is seen, not validation'):
        validate_seeds([2], 'validation', path)
    assert validate_seeds([2, 3], 'seen', path)['split'] == 'seen'
    assert validate_seeds([4], 'validation', path)['split'] == 'validation'

    data, _ = load_registry(path)
    assert data['revision'] == 2
    assert data['history'][-1]['seeds'] == [2, 3]
    assert data['history'][-1]['run'] == {'candidate': 'challenger'}
    covered = sorted(s for e in data['entries'] if e['end'] is not None
                     for s in range(e['start'], e['end']))
    assert covered == list(range(10))


def test_admission_requires_provenance_and_leaves_no_lock(tmp_path):
    path = registry(tmp_path, entry('reserved', 0, 10, 'validation'))
    with pytest.raises(ValueError, match='provenance'):
        admit_run([1], 'validation', None, path)
    with pytest.raises(ValueError):
        admit_run([1, 9000000], 'validation', {'run': 'x'}, path)
    assert not (tmp_path / 'registry.json.lock').exists()
    assert load_registry(path)[0]['revision'] == 1


def test_non_validation_splits_are_checked_but_not_consumed(tmp_path):
    path = registry(tmp_path, entry('dev', 0, 10, 'dev'))
    admit_run([1], 'dev', {'run': 'x'}, path)
    assert load_registry(path)[0]['revision'] == 1
    assert validate_seeds([1], 'dev', path)['split'] == 'dev'


def test_metadata_pins_the_registry_version_for_the_report():
    metadata = validate_seeds([1000], 'dev')
    assert metadata['registry_schema'] == 1
    assert metadata['registry_sha256'] == load_registry()[1]
    assert metadata['competitive'] is True
    assert validate_seeds([314159], 'diagnostic')['competitive'] is False
