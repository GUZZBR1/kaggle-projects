# Animal strategy sweep

Issue #2 was evaluated against the immutable v000 opponent set used by
`experiments/results/m1-v000`. Each candidate was built from the current
policy with only `animal_target` and `animal_type` overridden.

## Matrix smoke

The complete 12-cell matrix used fixed seeds `1000:1009` (100 games per
configuration, two seats against five opponents):

| Rank | Animal | Target | Score | CI95 | Mean margin |
|---:|---|---:|---:|---|---:|
| 1 | COW | 6 | 80.0% | [0.80, 0.80] | 27,841 |
| 2 | SHEEP | 3 | 80.0% | [0.80, 0.80] | 21,467 |
| 3 | SHEEP | 6 | 79.0% | [0.77, 0.80] | 22,999 |
| 4 | COW | 3 | 78.0% | [0.74, 0.80] | 19,936 |
| 5 | GOOSE | 0 | 75.0% | [0.70, 0.80] | 219 |
| 6 | COW | 0 | 75.0% | [0.70, 0.80] | 219 |
| 7 | SHEEP | 0 | 75.0% | [0.70, 0.80] | 219 |
| 8 | GOOSE | 3 | 73.0% | [0.67, 0.78] | 10,468 |
| 9 | SHEEP | 9 | 68.0% | [0.64, 0.73] | 11,528 |
| 10 | COW | 9 | 65.0% | [0.60, 0.71] | 11,941 |
| 11 | GOOSE | 6 | 49.0% | [0.43, 0.56] | 1,890 |
| 12 | GOOSE | 9 | 48.0% | [0.41, 0.57] | -1,116 |

## Full validation

The two leaders were rerun with fixed seeds `1000:1099` (1,000 games each,
100 seed blocks, both seats):

| Candidate | Score | CI95 | Mean margin | Failures |
|---|---:|---|---:|---:|
| `animal_type=COW`, `animal_target=6` | 79.4% | [0.788, 0.799] | 28,909 | 0 |
| `animal_type=SHEEP`, `animal_target=3` | 78.4% | [0.774, 0.792] | 19,835 | 0 |

For comparison, the immutable `m1-v000` report scores 72.3% on the same
opponent set. This is not a causal estimate of animals alone because the
current policy also contains the previously merged market and endgame work;
the within-sweep comparison isolates the animal parameters.

The selected recommendation is `COW×6`. The production default remains
`animal_target=0` until this challenger is promoted in a separate change;
`versions/v000` remains immutable.
