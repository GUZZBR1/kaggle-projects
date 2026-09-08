# Issue #22 — o que a telemetria diária mostrou

Medição feita com a arena corrigida (ver "Ressalva" no fim). 30 seeds de `dev`
(`1000:1030`), dois assentos, adversário `opponents/public/cok_v10`, backend
`fast`, 60 partidas. Todos os agregados diários reconciliam com os totais
auditados das mesmas partidas: `reconciliation_problems: []`.

## Resultado

| | valor |
|---|---:|
| Partidas | 60 |
| Score | **0.000** (CI95 [0.0, 0.0]) |
| Margem média | **−105.354** |
| Nosso dinheiro final (assento 0 / 1) | 37.304 / 37.030 |
| `cok_v10` final (assento 0 / 1) | 144.494 / 140.548 |

Perdemos as 60 partidas, nos dois assentos. Não é variância: é uma diferença
de aproximadamente 3,8× no dinheiro final.

## A hipótese da issue, respondida

A #22 perguntou se o déficit vem de liquidez inicial, capital de giro,
alocação de mão de obra, pressão de preço, pressão de estoque ou desperdício
de execução. A telemetria elimina quatro das seis.

**Não é desperdício de execução.** 24.960 ordens de mercado pedidas, 24.960
executadas. Nenhuma inválida, truncada ou falha. `no_effect_actions = 0`.

**Não é pressão de estoque.** `overflow_items = 0` na liga inteira; sobra
média de 2,1 itens por partida.

**Não é pressão de preço.** Preços realizados saudáveis e coerentes com o
modelo: STRAWBERRY 196,6/unidade, MELON 160,0, TOMATO 121,8.

**É liquidez inicial, e o mecanismo é visível dia a dia:**

| dia | caixa fim | receita | mãos (média) | plantios | colheitas | ações PASS |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 306 | 0 | 7,67 | 21,0 | 0 | 65,0 |
| 1 | 252 | 0 | 7,67 | 2,0 | 0 | 90,0 |
| 2 | 250 | 0 | 1,92 | 0 | 0 | 13,0 |
| 3–9 | **250** | **0** | **0,00** | **0** | **0** | **1,0** |
| 10 | 1.980 | 4.153 | 0,00 | 0 | 7,0 | 0 |
| 11 | 760 | 612 | 7,67 | 13,8 | 8,0 | 29,8 |

No dia 0 o agente contrata 8 mãos e planta 21 tiles. No dia 2 o caixa chega a
250 e ele perde toda a mão de obra. **Dos dias 3 ao 10 a fazenda fica
completamente parada**: zero mãos, zero plantios, zero colheitas, uma única
ação por dia. São **8 dias de 30 — 27% da temporada — com a fazenda insolvente
e ociosa**, esperando a primeira colheita, que só chega no passo 254 (dia 10).

O caixa mínimo da temporada inteira é 250, e é atingido já no dia 2.

Depois da primeira receita o agente se recupera e chega a 37k, mas recontrata
8 mãos no dia 11 e o caixa volta a cair para 631 no mesmo dia — o mesmo erro,
em escala menor. Só chegamos a 2 quadrantes desbloqueados na temporada toda.

## Leitura

O planner compra capacidade de produção antes de ter receita para sustentá-la,
e o ciclo da cultura é mais longo do que o caixa inicial aguenta. O custo não é
apenas o dinheiro gasto: são os 8 dias de produção perdidos, num jogo de 30
dias. Nenhuma melhoria de preço, roteamento ou armazenamento move esse número
enquanto a abertura continuar insolvente.

Isso é o que a #22 se propôs a identificar. A implementação de X-LIQ está
explicitamente fora do escopo dela e não foi feita aqui; a evidência acima é a
entrada para essa decisão.

## Ressalva metodológica

A primeira execução deste diagnóstico deu score 0,75 e margem −22.208, e estava
errada. A arena tinha deixado de repassar `step` ao assento 1, e o `cok_v10`
replica um traço de ações indexado inteiramente por `step`: sem ele, terminava
com 0 de dinheiro sempre que sentava no assento 1. O resultado lia como uma
vitória e uma derrota por seed, o que é assinatura de efeito de assento, não de
estratégia. Corrigido em `565b6d9`; os números acima são posteriores à correção.
Ao ler telemetria de adversário, uma métrica idêntica por assento merece
desconfiança antes de virar conclusão.
