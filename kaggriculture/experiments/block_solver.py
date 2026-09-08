"""Generate market or production-action blocks and evaluate their arrival states by fixed continuation.

All search and the disjoint check use registered development seeds. The output is
an experimental tape, never a promotion recommendation. Prefix replay is used to
restore the same frontier in a fresh process for each game; no private opponent
state or fitted heuristic is supplied to the generated agent.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import statistics
import time

from arena.agents import agent_hash
from arena.paired import check_spec
from arena.engine import fingerprint as engine_fingerprint
from arena.parallel import matches
from arena.seeds import validate_seeds, parse_seeds
from eval.comparison import digest
from eval.ladder import delta_win
from eval.pairing import paired_rows
from experiments.tape_agent import build
from experiments.tape_harvest import tape_digest
from experiments.production_mutations import production_mutations

TURNS = 719
BLOCK = 72
NO_ORDER = ['SELL', 'WHEAT', 0]


def block_end(start, days=3):
    if type(start) is not int or start < 0 or start >= TURNS or start % BLOCK:
        raise ValueError('Start must be a three-day boundary in [0, 719)')
    if days not in (3, 6):
        raise ValueError('Blocks must span three or six days (the terminal block is truncated)')
    return min(TURNS, start + days * 24)


def arrival_state(observation, seat):
    """Lossless own farm/private state, including positions, crop ages and inventories.

    Money is a diagnostic component, not the scalar objective. Value is measured
    by continuing the fixed suffix to the terminal win/loss/tie outcome.
    """
    if observation['player'] != seat:
        raise ValueError('Arrival observation belongs to a different seat')
    state = {key: copy.deepcopy(observation[key]) for key in ('step', 'day', 'hour', 'market', 'town')}
    state.update(farm=copy.deepcopy(observation['farms'][seat]),
                 private=copy.deepcopy(observation['private']))
    return {'sha256': digest(state), 'state': state}


def mutations(actions, start, end, count, rng, excluded=()):
    """Local market edits; prefix, suffix and worker actions remain exactly fixed."""
    if len(actions) != TURNS or not 0 <= start < end <= TURNS or count < 1:
        raise ValueError('Require a complete tape, bounded block and positive proposal count')
    candidates = []
    for turn in range(start, end):
        orders = actions[turn].get('market', [])
        for slot, order in enumerate(orders[:10]):
            if not isinstance(order, list) or len(order) < 3 or order[0] != 'SELL':
                continue
            if type(order[2]) is not int or order[2] <= 0:
                continue
            if slot > 0:
                candidates.append(('front', turn, slot, None))
            for quantity in sorted({max(1, order[2] // 2), order[2] * 2} - {order[2]}):
                candidates.append(('quantity', turn, slot, quantity))
            for target in (turn - 1, turn + 1):
                if start <= target < end and len(actions[target].get('market', [])) < 10:
                    candidates.append(('shift', turn, slot, target))
        if len(orders) > 1:
            candidates.append(('rotate', turn, None, None))
    rng.shuffle(candidates)
    candidates = [('block_order', start, None, direction) for direction in (1, -1, 0)] + candidates
    seen, result = set(excluded) | {tape_digest(actions)}, []
    for kind, turn, slot, value in candidates:
        tape = copy.deepcopy(actions)
        orders = tape[turn].setdefault('market', [])
        if kind == 'block_order':
            for action in tape[start:end]:
                market = action.get('market', [])
                if len(market) > 1:
                    action['market'] = (market[1:] + market[:1] if value == 1 else
                                        market[-1:] + market[:-1] if value == -1 else list(reversed(market)))
        elif kind == 'front':
            orders.insert(0, orders.pop(slot))
        elif kind == 'quantity':
            orders[slot][2] = value
        elif kind == 'shift':
            tape[value].setdefault('market', []).append(orders[slot])
            orders[slot] = NO_ORDER[:]
        else:
            orders.append(orders.pop(0))
        identity = tape_digest(tape)
        if identity in seen:
            continue
        seen.add(identity)
        result.append(dict(actions=tape, sha256=identity,
                           mutation=dict(kind=kind, turn=turn, slot=slot, value=value)))
        if len(result) == count:
            break
    return result


def fitness(rows):
    """Development selection: worst opponent score, then overall score; never coins."""
    by_opponent = {}
    for row in rows:
        by_opponent.setdefault(row['opponent'], []).append(row['score'])
    return (min(statistics.mean(values) for values in by_opponent.values()),
            statistics.mean(row['score'] for row in rows))


def evaluate(actions, directory, opponents, seeds, start, end, workers, provenance,
             expected_frontiers=None, expected_hashes=None, expected_environment=None):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    artifact = build(actions, directory / 'main.py', provenance=provenance)
    snapshots = sorted({start, end})
    jobs = [dict(candidate=str(artifact), opponent=opponent, seed=seed, seat=seat,
                 telemetry_enabled=False, replay_steps=snapshots,
                 replay=str(directory / f'snapshot-{index}-{seed}-{seat}.json'))
            for index, opponent in enumerate(opponents) for seed in seeds for seat in (0, 1)]
    rows, arrivals, frontiers = [], [], {}
    artifact_hash = agent_hash(str(artifact))
    for job, row in zip(jobs, matches(jobs, workers), strict=True):
        if row['failures'] or row['opponent_failures']:
            raise ValueError('Failed callbacks invalidate block evaluation')
        if row['candidate_hash'] != artifact_hash or (expected_hashes is not None
                and row['opponent_hash'] != expected_hashes[job['opponent']]):
            raise ValueError('Artifact changed during block evaluation')
        if expected_environment is not None and row['environment'] != expected_environment:
            raise ValueError('Environment changed during block evaluation')
        replay_path = Path(job['replay'])
        replay = json.loads(replay_path.read_text())
        observations = {turn['step']: turn['observations'][row['seat']] for turn in replay['turns']}
        if set(observations) != set(snapshots):
            raise ValueError('Block evaluation did not reach every requested boundary')
        key = (row['seed'], row['seat'], row['opponent'])
        frontiers[key] = digest(observations[start])
        if expected_frontiers is not None and frontiers[key] != expected_frontiers.get(key):
            raise ValueError('Candidate did not start from the same frontier')
        arrivals.append(dict(seed=row['seed'], seat=row['seat'], opponent=row['opponent'],
                             frontier_sha256=frontiers[key], end=end,
                             arrival=arrival_state(observations[end], row['seat']),
                             continuation_score=row['score'], money_diagnostic=row['money'],
                             margin_diagnostic=row['margin']))
        rows.append(row)
        replay_path.unlink()  # The compact, own-state record below replaces the transient replay.
    paired_rows(rows, rows)
    (directory / 'matches.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in rows))
    (directory / 'arrivals.json').write_text(json.dumps(arrivals) + '\n')
    return dict(rows=rows, frontiers=frontiers, fitness=fitness(rows), artifact=str(artifact),
                artifact_hash=artifact_hash)


def search(source, output, *, tape_index=0, start=648, days=3, proposals=4, rounds=2,
           opponents, seeds, check_seeds, workers=4, search_seed=771, mutation_space='market'):
    started = time.perf_counter()
    if mutation_space not in ('market', 'production'):
        raise ValueError('Unknown mutation space')
    end = block_end(start, days)
    seeds, check_seeds, opponents = list(seeds), list(check_seeds), list(opponents)
    if not opponents or len(set(opponents)) != len(opponents) or workers < 1 or proposals < 1 or rounds < 1:
        raise ValueError('Require distinct opponents, positive workers, proposals and rounds')
    if len(seeds) < 2 or len(check_seeds) < 2 or set(seeds) & set(check_seeds):
        raise ValueError('Require at least two disjoint development seeds for search and check')
    registry = {'search': validate_seeds(seeds, 'dev'), 'check': validate_seeds(check_seeds, 'dev')}
    source = Path(source)
    raw = source.read_bytes()
    library = json.loads(raw)
    if isinstance(library, dict):
        library = library['tapes']
    if type(tape_index) is not int or not 0 <= tape_index < len(library):
        raise ValueError('Tape index outside source library')
    initial = library[tape_index]
    initial = initial['actions'] if isinstance(initial, dict) else initial
    if len(initial) != TURNS or not all(isinstance(action, dict) for action in initial):
        raise ValueError('Source must contain a complete 719-action tape')
    hashes = {opponent: check_spec(opponent) for opponent in opponents}
    source_hash = hashlib.sha256(raw).hexdigest()
    source_manifest = source.parent / 'main.manifest.json'
    provenance = dict(source=str(source.resolve()), source_sha256=source_hash, tape_index=tape_index,
                      initial_tape_sha256=tape_digest(initial))
    if source_manifest.is_file():
        manifest = json.loads(source_manifest.read_text())
        provenance.update(source_url=manifest.get('source_url'), license=manifest.get('license'))
    credit = json.dumps(provenance, sort_keys=True)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    plan = dict(schema_version=1, kind=f'{mutation_space}_block_local_search', mutation_space=mutation_space, split='dev',
                created_at=datetime.now(timezone.utc).isoformat(), source=provenance,
                start=start, end=end, days=days, proposals=proposals, rounds=rounds,
                seeds=seeds, check_seeds=check_seeds, search_seed=search_seed,
                opponents=opponents, opponent_hashes=hashes, environment=engine_fingerprint(),
                registry=registry, objective=['worst_opponent_win_score', 'overall_win_score'],
                generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                production_mutations_sha256=hashlib.sha256(
                    Path(__file__).with_name('production_mutations.py').read_bytes()).hexdigest())
    (output / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    rng = random.Random(search_seed)
    history, visited = [], {tape_digest(initial)}
    try:
        common = dict(opponents=opponents, seeds=seeds, start=start, end=end, workers=workers,
                      provenance=credit, expected_hashes=hashes, expected_environment=plan['environment'])
        original = evaluate(initial, output / 'baseline-search', **common)
        incumbent, measured = copy.deepcopy(initial), original
        accepted = []
        for generation in range(rounds):
            generator = mutations if mutation_space == 'market' else production_mutations
            candidates = generator(incumbent, start, end, proposals, rng, excluded=visited)
            best_actions, best_result, best_mutation = incumbent, measured, None
            for index, proposal in enumerate(candidates):
                if proposal['sha256'] in visited:
                    continue
                visited.add(proposal['sha256'])
                assert proposal['actions'][:start] == initial[:start]
                assert proposal['actions'][end:] == initial[end:]
                result = evaluate(proposal['actions'], output / f'round-{generation}-proposal-{index}',
                                  expected_frontiers=original['frontiers'], **common)
                # Strict pairing checks the complete context, engine and adapters as well as seeds.
                delta = delta_win(original['rows'], result['rows'], ratings={})
                history.append(dict(round=generation, mutation=proposal['mutation'],
                    tape_sha256=proposal['sha256'], artifact_hash=result['artifact_hash'],
                    fitness=result['fitness'], delta_from_initial=delta['all'],
                    ineffective_unit_actions=sum(row['audit'].get('no_effect_actions', 0) for row in result['rows'])))
                print(f"round={generation} proposal={index} fitness={result['fitness']}", flush=True)
                if result['fitness'] > best_result['fitness']:
                    best_actions, best_result, best_mutation = proposal['actions'], result, proposal['mutation']
            if best_mutation is not None:
                accepted.append(best_mutation)
            incumbent, measured = best_actions, best_result
        # Freeze the chosen tape BEFORE inspecting the disjoint check. No second selection follows it.
        selected_hash = tape_digest(incumbent)
        (output / 'selection.json').write_text(json.dumps(dict(tape_sha256=selected_hash,
            fitness=measured['fitness'], accepted=accepted, history=history), indent=2) + '\n')
        common['seeds'] = check_seeds
        check_baseline = evaluate(initial, output / 'baseline-check', **common)
        check_candidate = evaluate(incumbent, output / 'candidate-check',
                                   expected_frontiers=check_baseline['frontiers'], **common)
        check = delta_win(check_baseline['rows'], check_candidate['rows'], ratings={})
        # Package the exact standalone file measured above, with the source tape and edit lineage.
        final_source = Path(check_candidate['artifact']).read_bytes()
        (output / 'main.py').write_bytes(final_source)
        (output / 'tapes.json').write_text(json.dumps({'tapes': [dict(actions=incumbent,
            sha256=selected_hash, provenance=provenance, mutations=accepted)]}) + '\n')
        manifest = dict(schema_version=1, kind=plan['kind'], sha256=hashlib.sha256(final_source).hexdigest(),
                        tape_sha256=selected_hash, source=provenance, mutations=accepted,
                        block={'start': start, 'end': end}, plan_sha256=digest(plan),
                        split='dev', release_status='not_validated')
        (output / 'main.manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        report = dict(plan=plan, evaluated_mutations=len(history), accepted_mutations=accepted,
                      initial_fitness=original['fitness'], selected_fitness=measured['fitness'],
                      selected_tape_sha256=selected_hash, check=check,
                      wall_seconds=time.perf_counter() - started, release_status='not_validated')
        (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        return report
    except Exception as exc:
        (output / 'failure.json').write_text(json.dumps(dict(error=str(exc),
            evaluated_mutations=len(history), wall_seconds=time.perf_counter() - started), indent=2) + '\n')
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation-space', choices=('market', 'production'), default='market')
    parser.add_argument('--source', required=True, help='JSON list of tapes or a tapes envelope')
    parser.add_argument('--tape-index', type=int, default=0)
    parser.add_argument('--start', type=int, default=648)
    parser.add_argument('--days', type=int, choices=(3, 6), default=3)
    parser.add_argument('--proposals', type=int, default=4)
    parser.add_argument('--rounds', type=int, default=2)
    parser.add_argument('--search-seed', type=int, default=771)
    parser.add_argument('--opponents', required=True)
    parser.add_argument('--seeds', default='1000:1004')
    parser.add_argument('--check-seeds', default='1004:1008')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--output', required=True)
    args = vars(parser.parse_args())
    args['opponents'] = args['opponents'].split(',')
    args['seeds'] = parse_seeds(args['seeds'])
    args['check_seeds'] = parse_seeds(args['check_seeds'])
    report = search(**args)
    print(json.dumps({key: report[key] for key in ('evaluated_mutations', 'accepted_mutations',
        'initial_fitness', 'selected_fitness', 'wall_seconds', 'release_status')}, indent=2))
    print(json.dumps(report['check']['all'], indent=2))


if __name__ == '__main__':
    main()
