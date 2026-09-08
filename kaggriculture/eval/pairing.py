"""Evidence checks shared by economic and wins-only paired comparisons."""
import json


def paired_rows(baseline, candidate):
    def keyed(rows):
        result = {}
        required = ('seed', 'seat', 'opponent', 'candidate_hash', 'opponent_hash',
                    'configuration', 'environment', 'backend', 'failures',
                    'opponent_failures', 'score')
        for row in rows:
            missing = [field for field in required if field not in row]
            if missing:
                raise ValueError(f'Missing comparison evidence: {missing}')
            if type(row['seed']) is not int or row['seed'] < 0 or row['seat'] not in (0, 1):
                raise ValueError('Invalid seed or seat')
            if row['configuration'].get('seed', row['seed']) != row['seed']:
                raise ValueError('Configuration seed disagrees with match seed')
            if row['score'] not in (0, .5, 1):
                raise ValueError('A game must score 1, .5 or 0; margin is not a score')
            if not row['candidate_hash'] or not row['opponent_hash']:
                raise ValueError('Missing agent hash')
            if row['failures'] or row['opponent_failures']:
                raise ValueError('Callback failure invalidates comparison')
            key = (row['seed'], row['seat'], row['opponent'])
            if key in result:
                raise ValueError('Duplicate match keys')
            result[key] = row
        if not result:
            raise ValueError('Unpaired comparison: require nonempty legs')
        for field in ('candidate_hash', 'configuration', 'environment', 'backend'):
            if len({json.dumps({k: v for k, v in row[field].items() if k != 'seed'}
                                if field == 'configuration' else row[field], sort_keys=True) for row in rows}) != 1:
                raise ValueError(f'{field} changed during the league')
        opponents = {row['opponent'] for row in rows}
        for opponent in opponents:
            if len({r['opponent_hash'] for r in rows if r['opponent'] == opponent}) != 1:
                raise ValueError('opponent_hash changed during the league')
        expected = {(seed, seat, opponent) for seed in {r['seed'] for r in rows}
                    for seat in (0, 1) for opponent in opponents}
        if result.keys() != expected:
            raise ValueError('Unpaired comparison: require complete seed blocks and both seats')
        return result

    left, right = keyed(baseline), keyed(candidate)
    if left.keys() != right.keys():
        raise ValueError('Unpaired comparison: require identical seed/seat/opponent sets')
    for key, old in left.items():
        for field in ('opponent_hash', 'configuration', 'environment', 'backend'):
            if old[field] != right[key][field]:
                raise ValueError(f'Unpaired {field}: {key}')
    # Canonical order makes the deterministic bootstrap independent of row order.
    return ({key: left[key] for key in sorted(left)},
            {key: right[key] for key in sorted(right)})
