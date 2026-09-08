"""Propose a dated ladder rating for every pinned opponent, from the public leaderboard.

The rating that matters is the one the artifact itself would earn, and that is only
observable for an artifact we submitted ourselves. For everything else the honest
observation is the author team's rating, which bounds the artifact from above: a team's
active agent may be better than anything it has published, never worse in a way we can
detect. This script collects those bounds and says which kind each one is; it does not
write `opponents/ratings.json`, because promoting a bound to `author_current` is a claim
that the pinned artifact is still the author's newest published notebook, and that claim
belongs to a person reading the output.

    python scripts/refresh_ratings.py            # needs the kaggle CLI, authenticated

See `docs/RATINGS_REFRESH.md` for what to do with the result.
"""
import csv
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
COMPETITION = 'kaggriculture'


def leaderboard(directory):
    """Download today's public leaderboard and index it by member username."""
    subprocess.run(['kaggle', 'competitions', 'leaderboard', COMPETITION, '-d', '-p', directory],
                   check=True, stdout=subprocess.DEVNULL)
    archive = next(Path(directory).glob('*.zip'))
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(directory)
    path = sorted(Path(directory).glob('*.csv'))[-1]
    rows = list(csv.DictReader(path.open(encoding='utf-8-sig')))
    index = {}
    for row in rows:
        for user in row['TeamMemberUserNames'].split(','):
            index[user.strip().lower()] = row
    return path.name, len(rows), index


def newest_kernel(user):
    """The author's most recently run notebook in this competition, or None."""
    result = subprocess.run(
        ['kaggle', 'kernels', 'list', '--user', user, '--competition', COMPETITION,
         '--page-size', '20', '--sort-by', 'dateRun'],
        check=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        match = re.match(rf'({re.escape(user)}/\S+)\s', line, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def pinned():
    """Every pinned bundle, with the kernel it came from when it came from one."""
    for manifest in sorted((ROOT / 'opponents' / 'public').glob('*/main.manifest.json')):
        data = json.loads(manifest.read_text(encoding='utf-8'))
        kernel = data.get('kernel')
        yield manifest.parent.name, kernel, (kernel.split('/', 1)[0] if kernel else None)


def main():
    with tempfile.TemporaryDirectory() as directory:
        snapshot, teams, index = leaderboard(directory)
    print(f'# {snapshot}: {teams} teams\n')
    for bundle, kernel, user in pinned():
        if not user:
            print(f'{bundle}: pinned from a repository, not a notebook. No author username to '
                  f'attribute, so no bound exists. Leave it in `unrated`.')
            continue
        row = index.get(user.lower())
        if not row:
            print(f'{bundle}: author {user!r} does not appear on the leaderboard. '
                  f'Leave it in `unrated`.')
            continue
        newest = newest_kernel(user)
        kind = 'author_current' if newest and newest.lower() == kernel.lower() else \
               'author_upper_bound'
        superseded = '' if kind == 'author_current' else f' superseded by {newest}'
        print(json.dumps({bundle: {
            'rating': float(row['Score']), 'observed_at': row['LastSubmissionDate'][:10],
            'kind': kind,
            'source': f"author team {row['TeamName']!r} ({user}), rank {row['Rank']} of "
                      f"{teams}, public leaderboard snapshot {snapshot}",
            'note': f'{kernel}{superseded}'}}, ensure_ascii=False))
    print('\n# `observed_at` above is the team\'s last submission date. Use the date you '
          'pulled the snapshot instead when they differ: staleness is about when we looked.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
