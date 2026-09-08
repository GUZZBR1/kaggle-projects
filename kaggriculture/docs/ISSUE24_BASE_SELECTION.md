# Issue #24 — seleção da base pública

Amostra registrada de 100 seeds, que era o que faltava. Seeds `1000:1100`
(split `dev`), quatro candidatos × quatro famílias de adversário, dois
assentos, backend `fast`, **3.200 partidas**, **zero falhas de callback**, 100
blocos de seed por candidato. Decisão completa em `docs/issue24-base-selection.json`.

## Decisão

**Base selecionada: `cok_v10`** (família `public_adaptive_livestock_routes`),
único candidato dentro da tolerância de empate.

| candidato | piso (pior família) | CI95 inf. | desvio entre famílias | desequilíbrio | score agregado |
|---|---:|---:|---:|---:|---:|
| **cok_v10** | **0,995** | **0,985** | 0,002 | 0,005 | 0,874 |
| seyamalam_v21 | 0,005 | 0,000 | 0,469 | 0,995 | 0,626 |
| lonespear_v11 | 0,000 | 0,000 | 0,450 | 0,955 | 0,364 |
| **v002** | **0,000** | 0,000 | 0,021 | 0,045 | **0,136** |

O `cok_v10` é o único com piso positivo, e é robusto e não apenas forte: 0,002
de desvio entre famílias e 0,005 de desequilíbrio de confronto.

O `seyamalam_v21` ilustra por que o critério é pior família e não agregado.
Ele vence `lonespear_v11` e `v002` em 100%, mas perde para o `cok_v10` em
99,5%. Agregado 0,626 esconde um piso de 0,005. Selecionar por agregado teria
sido plausível e errado.

## O v002 não se sustenta como base

| adversário | score do v002 | margem |
|---|---:|---:|
| cok_v10 | 0,000 | −110.676 |
| seyamalam_v21 | 0,000 | −97.297 |
| lonespear_v11 | 0,045 | −43.037 |

Perde **todas** as partidas contra duas das três famílias rivais. Isso é
consistente com o diagnóstico da #22 (`docs/ISSUE22_DAILY_ECONOMICS.md`): 27%
da temporada insolvente e parada, com execução, preço e estoque limpos. Não é
um ajuste de parâmetro que falta; é a família estratégica.

## Correção na regra de seleção

Cada candidato encontrava a si mesmo na lista de adversários, e o espelho dá
exatamente 0,500 por construção, nos dois assentos. Isso **fixava o piso em
0,500 para qualquer candidato que nunca perdesse uma família**, entregando a
decisão aos desempates — e o desempate por menor variância *penaliza quem
domina*, porque o 0,500 do espelho fica longe dos scores reais.

O espelho passou a ser excluído do resumo por família. Efeito nos números:

| candidato | piso antes | piso depois | desvio antes | desvio depois |
|---|---:|---:|---:|---:|
| cok_v10 | 0,500 | 0,995 | 0,216 | 0,002 |
| seyamalam_v21 | 0,005 | 0,005 | 0,413 | 0,469 |
| v002 | 0,000 | 0,000 | 0,211 | 0,021 |

**A decisão não muda**, porque os demais tinham piso abaixo de 0,500 e o
`cok_v10` venceria de qualquer modo. Era um defeito latente, não um erro de
resultado: ele só decidiria errado se dois candidatos dominassem todas as
famílias rivais. Reanalisado a partir das mesmas 3.200 partidas gravadas, sem
nova execução. `analyze_tournament` agora também recusa um pool que deixe um
candidato com menos de duas famílias rivais após a exclusão.

## Pendência que não é minha para decidir

Selecionar o `cok_v10` como base **mais robusta** não é o mesmo ato que
submetê-lo. `opponents/manifest.json` registra `usage: "benchmark opponent
only"`, e o bundle é Apache-2.0 de terceiro. Adotá-lo como nossa submissão
levanta uma questão de licenciamento e de regras da competição que precisa de
decisão humana, não de evidência estatística. Esta issue pedia a seleção, e a
seleção está feita.
