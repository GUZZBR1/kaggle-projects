"""Selection by worst family is the whole point of screening; assert it directly."""
from experiments.tape_screen import build_agents, rank


def payload(rows, labels=None):
    return {'rows': rows, 'tapes': labels or {}}


def row(tape, opponent, score, margin=0., seed=1000, seat=0):
    return {'tape': tape, 'opponent': opponent, 'seed': seed, 'seat': seat, 'score': score,
            'margin': margin, 'money': 0., 'opponent_money': 0., 'failures': 0,
            'opponent_failures': 0}


def test_a_tape_is_ranked_by_its_weakest_matchup_not_its_average():
    """A tape that farms a weak family and folds to a strong one is not robust."""
    lopsided = [row('lopsided', 'strong', 0.), row('lopsided', 'weak', 1.)]
    steady = [row('steady', 'strong', 0.4), row('steady', 'weak', 0.6)]

    table = rank(payload(lopsided + steady))

    assert [entry['tape'] for entry in table] == ['steady', 'lopsided']
    assert table[0]['worst_family'] == 0.4
    assert table[0]['score'] == table[1]['score'] == 0.5, 'the aggregate cannot separate them'


def test_margin_breaks_a_tie_that_score_cannot():
    rows = [row('rich', 'a', 1., margin=9000.), row('poor', 'a', 1., margin=10.)]
    assert [entry['tape'] for entry in rank(payload(rows))] == ['rich', 'poor']


def test_ranking_carries_the_provenance_of_each_tape():
    labels = {'t': {'team': 'alice', 'episode': 42, 'money': 120.}}
    entry = rank(payload([row('t', 'a', 1.)], labels))[0]
    assert entry['team'] == 'alice' and entry['episode'] == 42
    assert entry['per_opponent'] == {'a': 1.}


def test_agents_are_named_by_digest_and_built_once(tmp_path):
    actions = [{'farmer': ['NORTH'], 'hands': [], 'market': []} for _ in range(719)]
    tapes = [{'sha256': 'abc123def456789', 'actions': actions, 'episode': 1, 'seat': 0,
              'money': 5.}]

    paths = build_agents(tapes, tmp_path)
    stamp = (tmp_path / 'abc123def456.py').stat().st_mtime_ns
    build_agents(tapes, tmp_path)

    assert paths['abc123def456789'] == str(tmp_path / 'abc123def456.py')
    assert (tmp_path / 'abc123def456.py').stat().st_mtime_ns == stamp
