def parse_seeds(value):
    if ':' in value:
        start, end = map(int, value.split(':'))
        if end <= start:
            raise ValueError('Seed range must be nonempty and half-open, e.g. 1000:1100')
        return list(range(start, end))
    seeds = [int(s) for s in value.split(',')]
    if len(set(seeds)) != len(seeds):
        raise ValueError('Duplicate seeds would inflate evidence')
    return seeds
