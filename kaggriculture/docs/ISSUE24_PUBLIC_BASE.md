# Issue #24 — seleção de base pública

Issue #24, P0.5. **Resultado: base selecionada — `cok_v10`.** A amostra registrada de
100 seeds confirma a seleção que o smoke de 2 seeds já apontava.

## O que foi testado

Quatro candidatos disputam o papel de base congelada: o artefato interno `v002` e os três
oponentes públicos pinados na #27. A pergunta não é quem tem o melhor score agregado, e sim
quem sustenta o pior confronto — um candidato que arrasa duas famílias e apanha de uma
terceira é uma base frágil, porque a família que o derrota existe no ladder.

Por isso `experiments/public_base_tournament.py` seleciona pelo **limite inferior do IC95 do
score da pior família**, nunca pelo agregado. O agregado aparece nos resultados apenas como
contraste.

Antes de qualquer partida, cada bundle passa por dois portões:

- **Proveniência** (`validate_entry`): hash SHA-256 do arquivo, licença verificada, engine
  pinada (`kaggle_environments==1.32.7` + hash do interpretador), linhagem declarada e
  caminho contido no projeto. Falha aqui aborta antes do primeiro jogo.
- **Compatibilidade de relógio** (`compatibility_check`): o mesmo bundle é chamado com `step`
  ausente e com `step=None`, e as duas ações precisam ter hash idêntico. Um bundle que muda de
  comportamento quando a chave opcional some não é evidência confiável.

Os quatro candidatos passaram nos dois portões.

## Protocolo

- Split `dev`, seeds `1000:1100` (100 seeds), ambos os assentos, backend `fast`.
- Cada candidato enfrenta as **quatro** famílias do pool, inclusive a própria.
- 800 partidas por candidato, **3.200 no total**. Zero falhas de callback.
- `min_seed_blocks=100`, `tie_tolerance=0.05`.

> A diagonal da matriz é o espelho (candidato contra si mesmo) e vale exatamente 0.500 por
> simetria. Ela entra no cálculo porque manter o pool idêntico para todos os candidatos é o
> que torna as linhas comparáveis entre si; excluí-la daria um conjunto de oponentes
> diferente para cada candidato.

## Resultados

Score por família (linha = candidato, coluna = família do oponente):

| Candidato | `internal_adaptive_planner` | `public_adaptive_livestock_routes` | `route_market_recovery` | `standing_on_work_livestock` | Pior família | Agregado |
|---|---:|---:|---:|---:|---:|---:|
| `cok_v10` | 1.000 | *0.500* | 0.995 | 1.000 | **0.500** | **0.874** |
| `seyamalam_v21` | 1.000 | 0.005 | *0.500* | 1.000 | 0.005 | 0.626 |
| `lonespear_v11` | 0.985 | 0.000 | 0.000 | *0.500* | 0.000 | 0.371 |
| `v002` | *0.500* | 0.000 | 0.000 | 0.015 | 0.000 | 0.129 |

*(em itálico: o confronto espelho)*

A hierarquia é **estritamente transitiva** — não há ciclo pedra-papel-tesoura:
`cok_v10` > `seyamalam_v21` > `lonespear_v11` > `v002`.

Comparação pareada contra `v002`, por seed e assento. A margem absoluta é do próprio
candidato contra o pool inteiro e **não** é um delta — as duas colunas respondem perguntas
diferentes:

| Candidato | Δ score (pareado) | IC95 | Δ dinheiro (pareado) | Margem absoluta |
|---|---:|---:|---:|---:|
| `cok_v10` | **+0.7450** | [+0.7388, +0.7500] | +62.364 | +43.274 |
| `seyamalam_v21` | +0.4975 | [+0.4913, +0.5025] | +52.355 | +28.737 |
| `lonespear_v11` | +0.2425 | [+0.2300, +0.2500] | +30.095 | −4.833 |
| `v002` (baseline) | — | — | — | −67.177 |

`lonespear_v11` ilustra a diferença: ganha de `v002` no pareado (+30 mil), mas fecha com
margem absoluta negativa, porque apanha de `cok_v10` e de `seyamalam_v21`.

## Leitura

**`cok_v10` é a base selecionada, e por uma margem que não depende de escolha de métrica.**
Ele vence todas as outras três famílias (0.995 a 1.000); o único resultado dele abaixo de
0.99 é o próprio espelho. Isso significa que seu piso de pior família — os 0.500 que
determinam a seleção — é estrutural, imposto pela simetria do espelho e não por um adversário
que o derrote. Nenhum outro candidato chega perto: o segundo colocado apanha de `cok_v10`
com score 0.005.

**`v002` é o mais fraco dos quatro.** Perde para as três famílias públicas (0.000, 0.000,
0.015) e fecha com margem média de −67 mil. O planner interno não é competitivo contra o que
já está publicado, e é isso que justifica a #24 existir: adotar uma base externa é decisão
baseada em medição, não preferência.

Vale registrar o que este número **não** diz. `v002` aqui é o artefato congelado
`versions/v002/main.py`, não a árvore de trabalho atual do agente; medições posteriores do
planner não são comparáveis a esta linha sem repetir o protocolo.

## Artefatos

- Decisão completa (com telemetria diária, 460 KB): `experiments/results/issue24-public-base-dev/decision.json` — não versionado, `experiments/results/` é gitignored.
- Resumo auditável versionado: `docs/issue24-public-base.json`.
- Smoke anterior de 2 seeds (mesma seleção): `experiments/results/issue24-public-base-smoke/`.

Reprodução:

```
python experiments/public_base_tournament.py --output <dir> --seeds 1000:1100 --workers 10
```

Executado em 2026-09-08, ~57 min com 10 workers.
