"""Single versioned seed registry, including atomic pre-run consumption."""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / 'seed_registry.json'
SPLITS = ('dev', 'seen', 'validation', 'diagnostic')


def parse_seeds(value):
    if ':' in value:
        start, end = map(int, value.split(':'))
        if end <= start:
            raise ValueError('Seed range must be nonempty and half-open, e.g. 1000:1100')
        return list(range(start, end))
    seeds = [int(s) for s in value.split(',')]
    if len(set(seeds)) != len(seeds):
        raise ValueError('Duplicate seeds would inflate evidence')
    if not seeds or any(s < 0 for s in seeds):
        raise ValueError('Seeds must be nonnegative integers')
    return seeds


def load_registry(path=REGISTRY):
    raw = Path(path).read_bytes()
    registry = json.loads(raw)
    if registry.get('schema_version') != 1 or type(registry.get('revision')) is not int:
        raise ValueError('Unsupported registry schema/revision')
    entries = sorted(registry['entries'], key=lambda r: r['start'])
    previous_end = 0
    ids = set()
    for entry in entries:
        start, end = entry['start'], entry['end']
        if (type(start) is not int or start < 0 or (end is not None and
                (type(end) is not int or end <= start)) or start < previous_end):
            raise ValueError('Invalid or overlapping registry intervals')
        if (entry['id'] in ids or not entry.get('provenance') or
                entry['classification'] not in (*SPLITS, 'holdout')):
            raise ValueError('Registry requires unique IDs, provenance and valid classification')
        ids.add(entry['id'])
        previous_end = float('inf') if end is None else end
        if end is None and entry['classification'] != 'holdout':
            raise ValueError('Only holdout can be unbounded')
    holdout = [r for r in entries if r['classification'] == 'holdout']
    if len(holdout) != 1 or holdout[0]['start'] != 9000000 or holdout[0]['end'] is not None:
        raise ValueError('Canonical holdout must remain protected at 9000000+')
    if registry.get('holdout_start') != 9000000:
        raise ValueError('Cannot move the protected holdout boundary')
    return registry, hashlib.sha256(raw).hexdigest()


def validate_seeds(seeds, split, path=REGISTRY):
    seeds = list(seeds)
    if (split not in SPLITS or not seeds or any(type(s) is not int or s < 0 for s in seeds)
            or len(seeds) != len(set(seeds))):
        raise ValueError('Require an explicit split and unique nonnegative seeds')
    registry, digest = load_registry(path)
    for seed in seeds:
        matches = [r for r in registry['entries'] if r['start'] <= seed
                   and (r['end'] is None or seed < r['end'])]
        if len(matches) != 1:
            raise ValueError(f'Unregistered seed {seed}; register with provenance before running')
        actual = matches[0]['classification']
        if actual != split:
            raise ValueError(f'Seed {seed} is {actual}, not {split}; holdout is never authorized here')
    return dict(registry_schema=1, registry_revision=registry['revision'], registry_sha256=digest,
                split=split, competitive=split != 'diagnostic')


@contextmanager
def registry_lock(path):
    lock = Path(str(path) + '.lock')
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        yield
    finally:
        os.close(fd)
        lock.unlink()


def admit_run(seeds, split, provenance, path=REGISTRY):
    """Burn reserved seeds BEFORE callbacks, including interrupted/failed runs.

    Subsequent reproduction is allowed only with split='seen'. A paired batch
    must declare all its candidate hashes in provenance before this admission.
    """
    seeds = list(seeds)
    if not provenance:
        raise ValueError('Run admission requires provenance')
    if split != 'validation':
        return validate_seeds(seeds, split, path)
    with registry_lock(path):
        metadata = validate_seeds(seeds, split, path)
        registry, _ = load_registry(path)
        revision = registry['revision'] + 1
        new_entries = []
        requested = set(seeds)
        for entry in registry['entries']:
            selected = sorted(s for s in requested if entry['start'] <= s
                              and (entry['end'] is None or s < entry['end']))
            if not selected:
                new_entries.append(entry)
                continue
            boundaries = sorted({entry['start'], entry['end'], *selected, *(s + 1 for s in selected)})
            segments = []
            for start, end in zip(boundaries, boundaries[1:]):
                kind = 'seen' if start in requested else entry['classification']
                if segments and segments[-1]['classification'] == kind:
                    segments[-1]['end'] = end
                else:
                    segments.append({**entry, 'id': f"{entry['id']}-r{revision}-{start}",
                                     'start': start, 'end': end, 'classification': kind,
                                     'provenance': entry['provenance'] + ([f'Consumed before run at registry revision {revision}'] if kind == 'seen' else [])})
            new_entries.extend(segments)
        registry['entries'] = new_entries
        registry['revision'] = revision
        registry['history'].append(dict(revision=revision, date=datetime.now(timezone.utc).isoformat(),
            reason='Reserved validation consumed before execution', seeds=seeds, run=provenance,
            previous_sha256=metadata['registry_sha256']))
        target = Path(path)
        temporary = target.with_suffix('.tmp')
        try:
            temporary.write_text(json.dumps(registry, indent=2) + '\n', encoding='utf-8')
            load_registry(temporary)
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
        metadata['consumption_revision'] = revision
        metadata['consumed_registry_sha256'] = load_registry(target)[1]
        return metadata
