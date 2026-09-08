"""The tape library is only useful if it refuses to lie about what it contains."""
import json

import pytest

from experiments.tape_harvest import extract, harvest, tape_digest


def replay(actions, seat=0):
    return {'format': 'kaggriculture-lab-v2',
            'turns': [{'step': i + 1, 'actions': [a if seat == 0 else {'farmer': ['PASS']},
                                                  a if seat == 1 else {'farmer': ['PASS']}],
                       'observations': []} for i, a in enumerate(actions)]}


def stream(head='NORTH'):
    return [{'farmer': [head], 'hands': [], 'market': []} for _ in range(719)]


def test_extract_takes_only_the_donors_own_actions():
    donor = stream('NORTH')
    assert extract(replay(donor, seat=0), 0) == donor
    assert extract(replay(donor, seat=1), 1) == donor
    # Reading the wrong seat must not silently return the opponent's stream.
    assert extract(replay(donor, seat=1), 0) != donor


def test_a_truncated_or_gapped_replay_is_refused():
    with pytest.raises(ValueError, match='719'):
        extract(replay(stream()[:100]), 0)
    broken = replay(stream())
    broken['turns'][17]['step'] = 999
    with pytest.raises(ValueError, match='not contiguous'):
        extract(broken, 0)


def test_identical_streams_share_one_identity():
    assert tape_digest(stream('NORTH')) == tape_digest(stream('NORTH'))
    assert tape_digest(stream('NORTH')) != tape_digest(stream('SOUTH'))


def test_harvest_refuses_to_overwrite_a_library(tmp_path):
    target = tmp_path / 'tapes.json'
    target.write_text('{}')
    with pytest.raises(FileExistsError):
        harvest(['challenger'], ['starter'], [1000], target)


def test_harvest_requires_donors_opponents_and_seeds(tmp_path):
    for donors, opponents, seeds in ((), ('starter',), (1000,)), (('challenger',), (), (1000,)), \
                                    (('challenger',), ('starter',), ()):
        with pytest.raises(ValueError, match='Require donors'):
            harvest(list(donors), list(opponents), list(seeds), tmp_path / f'{len(donors)}{len(opponents)}{len(seeds)}.json')


def test_a_real_harvest_keeps_only_wins_and_deduplicates(tmp_path):
    """End to end against the engine, small enough to stay a unit test.

    challenger beats starter, so the filter keeps those games; the tapes carry
    diagnostic margins and repeated streams collapse to one entry.
    """
    payload = harvest(['challenger'], ['starter'], [1000, 1001], tmp_path / 'lib.json',
                      workers=2, min_score=1.)
    assert payload['schema_version'] == 1
    assert payload['stats']['games'] == 4
    assert payload['stats']['kept'] == len(payload['tapes']) >= 1
    assert payload['stats']['kept'] + payload['stats'].get('duplicates', 0) \
           + payload['stats'].get('rejected_weak', 0) + payload['stats'].get('failed', 0) == 4
    for tape in payload['tapes']:
        assert len(tape['actions']) == 719
        assert tape['score'] == 1. and tape['margin'] > 0
        assert tape['sha256'] == tape_digest(tape['actions'])
        assert tape['sources'], 'every tape records which games produced it'
    assert [t['sha256'] for t in payload['tapes']] == sorted(t['sha256'] for t in payload['tapes'])
    assert json.loads((tmp_path / 'lib.json').read_text())['tapes']


def test_an_impossible_filter_yields_an_honest_empty_library(tmp_path):
    payload = harvest(['challenger'], ['starter'], [1000], tmp_path / 'none.json',
                      workers=2, min_score=2.)
    assert payload['tapes'] == []
    assert payload['stats']['rejected_weak'] == 2
