# Emendar blocos: a distância de junção prevê a perda

O passo que faltava do método público — comparar blocos na mesma fronteira em vez
de agentes inteiros — precisa de uma forma de saber se um bloco *cabe* onde vai
ser colado. Este documento mede se a nossa pontuação de estado de chegada serve.

## O problema

Um bloco não é portátil sozinho. Ele assume uma fazenda: peões contratados,
tiles plantados, mercadoria no galpão, o farmer numa posição. Colado depois de um
prefixo que deixa outra fazenda, suas ações endereçam coisas que não existem.

`experiments/tape_splice.py` mede isso. `fingerprint` registra o que o bloco
seguinte depende (dinheiro, posição do farmer, quantidade de peões, quadrantes,
tiles por tipo, galpão, sementes, carga nas mãos) e `join_distance` compara dois
mundos, com pesos que dizem o que um bloco **não consegue** recuperar dentro de
si: peões e quadrantes pesam mais que caixa e galpão.

## A validação

Quatro fitas do `thomas_t95`, todas as emendas cruzadas em três fronteiras
(144, 288, 432), contra o `kaitofukami_v48`, seed 1075. Para cada emenda,
comparamos o dinheiro final com o da fita do sufixo tocada inteira — a perda é o
custo da junção.

| corte | distância típica | perda típica |
|---:|---:|---:|
| 144 | 0,000 | ±1 moeda |
| 288 | 0,002 – 0,026 | −166 a −13.804 |
| 432 | 0,022 – 0,095 | −4.404 a −26.081 |

**Correlação distância × perda: −0,938** em 36 emendas.

A distância prevê a perda com força alta. É isso que torna uma busca viável: dá
para filtrar candidatos pela pontuação e só jogar os que sobrevivem, em vez de
rodar uma partida por combinação.

## O que os números dizem além da correlação

**No turno 144 várias emendas custam uma moeda.** A distância dá exatamente
0,000: nesse ponto essas fitas deixam a fazenda em estado idêntico, então os
blocos são livremente intercambiáveis. É a definição operacional de
"continuação compatível" — e explica por que os roteadores públicos decidem em
144: é onde trocar de plano ainda é gratuito.

**Quanto mais tarde o corte, mais caro.** No 432 até a melhor emenda perde 4.400
moedas. Uma fazenda diverge com o tempo, e um bloco tardio depende de uma
história que o prefixo não viveu. Isso limita onde uma biblioteca de blocos pode
ser montada — e é coerente com o roteador do `yhay`, cuja segunda decisão no
passo 648 é liquidação terminal, não troca de plano.

## Limites desta medição

Uma seed, um adversário, um assento, quatro fitas do mesmo doador. A correlação é
forte mas medida num regime estreito: fitas de doadores diferentes divergem mais
cedo e podem ter junções piores do que a distância sugere. Antes de usar isso
como filtro numa busca de verdade, vale repetir em várias seeds e com fitas de
procedências distintas — inclusive as do `yhay_router_0908`, que agora é o teto
medido do campo.
