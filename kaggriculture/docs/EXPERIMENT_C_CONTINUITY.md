# Experimento C — continuidade de execução no planner

Issue #15, P2. **Resultado: hipótese rejeitada. Não promover.**

## O que foi testado

O planner reavalia todos os jobs a cada turno e escolhe o máximo de
`value / (1 + travel * 0.65)`. Como o agente é um callback sem memória entre turnos,
"continuidade" não pode ser expressa com estado persistente sem violar o isolamento que o
projeto trata como propriedade de segurança (`arena/agents.py` cria namespace novo por
assento e partida, justamente para impedir vazamento de estado).

A formulação sem memória escolhida foi o caso mais defensável de compromisso: **um job que a
unidade pode executar agora, parada onde está, paga neste turno; qualquer job a distância `d`
não paga nada por `d` turnos.** O desconto de viagem sozinho subestima essa diferença, então
uma unidade em cima de uma rega de valor 65 é puxada para um `FEED` de valor 160 a um tile de
distância (`160/1.65 = 97 > 65`), gastando o turno andando em vez de completar trabalho.

O parâmetro `continuity_completion` multiplica o score de jobs com `travel == 0`. O default
é `1.0`, que é **exatamente inerte** — `tests/test_continuity.py::test_default_is_inert`
verifica igualdade turno a turno da política numa temporada completa.

## Protocolo

Comparação pareada via `eval.compare`. Baseline é esta mesma árvore com o bônus desligado,
o que isola uma única variável.

> Desvio consciente do plano: o plano especifica `v001` como baseline, mas a árvore já
> divergiu do artefato congelado (o `risk_posture` da #9 entrou depois). Parear contra `v001`
> confundiria continuidade com aquela mudança.

- Seeds: dev `1000:1100` (100 seeds), ambos os assentos.
- Oponentes: `starter`, `frozen/crop`, `frozen/animal`, `public/cok_v10`.
- 800 partidas por configuração, 3.200 no total. Zero falhas, zero ações sem efeito.

## Resultados

O mecanismo funciona como projetado — as unidades andam menos:

| Config | Bônus | Score | Fração de movimento |
|---|---:|---:|---:|
| baseline | 1.0 | **0.7488** | 0.5125 |
| bonus15 | 1.5 | 0.5625 | 0.5045 |
| bonus20 | 2.0 | 0.5613 | 0.4853 |
| bonus30 | 3.0 | 0.5675 | 0.4784 |

Mas a vitória pareada desaba, com CI95 excluindo zero com folga em todos os níveis:

| Config | Δ score pareado | CI95 | Δ dinheiro |
|---|---:|---|---:|
| bonus15 | −0.1862 | [−0.2062, −0.1650] | +857 |
| bonus20 | −0.1875 | [−0.2075, −0.1663] | +5.131 |
| bonus30 | −0.1812 | [−0.2025, −0.1588] | +5.577 |

O dinheiro **sobe** enquanto a vitória **cai** — exatamente o caso que o critério de decisão
da #15 antecipa ao dizer que margem não substitui vitória.

Por oponente (bonus30), a perda inteira vem de um único confronto:

| Oponente | Δ score | Δ dinheiro | Δ margem |
|---|---:|---:|---:|
| starter | +0.0000 | +11.900 | +11.897 |
| frozen/crop | +0.0000 | +11.854 | +11.921 |
| frozen/animal | **−0.7250** | −5.855 | −14.368 |
| **cok_v10** | **+0.0000** | +4.409 | +3.569 |

Contra `cok_v10` o delta é exatamente zero: continua **0/200**. A hipótese não toca o
problema competitivo que a V0.2 existe para resolver.

## Por que perde contra `frozen/animal`

Não é interação de mercado com a ração do oponente, como supus a princípio. Os preços de
venda realizados mostram outra coisa:

| vs `frozen/animal` | MELON |
|---|---|
| baseline | 102 unidades a $184,9 → $18.860 |
| bonus30 | 124 unidades a $128,0 → $15.872 |

**+22% de volume, −31% de preço, receita menor.** O melão tem a curva de glut mais punitiva
do jogo (`sq`, `above_target` 3,6). O bônus de continuidade aumenta a produtividade da
fazenda, e essa produtividade extra atravessa o joelho da quadrática e destrói mais valor do
que cria.

Contra `cok_v10` o mesmo bônus quase não move volume nem preço (85 a $158,3 → 88 a $156,9),
o que explica o delta zero ali.

Vale registrar que `adaptive_sales` já está ligado por default e mesmo assim o melão caiu
31%: o freio implementado na #3 atua no lado da venda e não impede o colapso quando é a
**produção** que cresce.

## Conclusão

Rejeitar, conforme o próprio critério do P2 ("sem melhora competitiva → rejeitar a hipótese
sem empilhar mais complexidade"). O parâmetro fica com default inerte, no mesmo espírito do
`sell_fraction` legado, para que a ablação continue reproduzível — mas não deve compor a V0.2.

O achado transferível é mais útil que o experimento: **produzir mais não é monotonicamente
bom neste jogo.** Qualquer mudança futura que aumente throughput precisa ser avaliada junto
do preço realizado, não só do volume.
