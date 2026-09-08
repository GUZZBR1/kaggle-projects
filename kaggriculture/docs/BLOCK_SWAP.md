# Blocos não são intercambiáveis, nem dentro da mesma procedência

Passo 1/4 da #39, e a resposta ao que o `OPPORTUNITY_SEARCH.md` deixou como único eixo
restante. A hipótese da issue era tratar blocos de três ou seis dias como **candidatos
intercambiáveis** entre fitas. Medida em vitória, ela é falsa — e a medição diz onde o
valor realmente está.

## O desenho

`--mutation-space swap` troca o bloco inteiro `[start, end)` do titular pelo mesmo bloco de
outra fita **da mesma biblioteca**, ou seja, da mesma procedência: as quatro fitas do
`yhay_router_0908`, saídas do mesmo solver do autor. Prefixo e sufixo ficam byte a byte, e o
`evaluate` recusa a avaliação se o estado que entra no bloco não for idêntico ao do titular.
Um doador que vencesse, venceria da mesma posição inicial.

`--days full` acrescenta a segunda forma: em vez de devolver ao titular no fim do bloco,
**compromete-se com a fita doadora até o fim da temporada**. É o que um roteador faz ao
escolher uma fita numa fronteira. As duas rodam na mesma ferramenta, com as mesmas seeds,
assentos e fronteira, então são comparáveis diretamente.

Onde as fitas divergem, medido antes de gastar partida: a fita 1 difere da fita 0 em todos
os blocos a partir do turno 144; as fitas 2 e 3 só divergem em 648:719, em 21 e 2 turnos.

## O resultado: 21 doadores, zero aceitos

Base: fita 0 do `yhay`. Adversários `thomas_t95` e `aberatozer_d5e3`, dois assentos, seeds
`dev` disjuntas por experimento, uma rodada.

| fronteira | forma | titular | melhor doador | delta de vitória | delta de moeda |
|---|---|---:|---:|---:|---:|
| 144:288 | bloco | 0,625 | 0,0625 | **−0,5625** | −17 963 |
| 288:432 | bloco | 0,250 | 0,3125 | 0,000 | −476 |
| 432:576 | bloco | 0,750 | 0,750 | 0,000 | −904 |
| 576:719 | bloco | 0,750 | 0,750 | 0,000 | −121 |
| 648:719 | bloco | 0,750 | 0,750 | 0,000 | −320 |
| 144:719 | sufixo | 0,625 | 0,625 | 0,000 (fita 1: **−0,5625**) | +24 |
| 288:719 | sufixo | 0,250 | 0,3125 | 0,000 | −219 |
| 432:719 | sufixo | 0,750 | 0,750 | 0,000 (fita 1: **−0,125**) | −186 |
| 648:719 | sufixo | 0,750 | 0,750 | 0,000 | −320 |

**Nenhum doador melhorou uma única partida.** Fora um único caso de +24 moedas, todos os 21
são iguais ou piores também em moeda. Trocar o bloco 144:288 pela versão da fita 1 custa
mais de meia vitória por partida. E comprometer-se com o sufixo em vez de devolver ao
titular não salva nada: em 432 o sufixo é *pior* que o bloco (−0,125 contra 0,000).

## Por que, medido de frente

Se a fita 1 é tão ruim, por que o autor a carrega? Porque o valor dela é inteiramente
**condicional**. A regra dele no turno 144 é uma só: se a cidade abriu um `YARN_STORE`, vá
para a fita 1. Auditei a regra com as duas fitas nuas, 16 seeds, dois adversários, dois
assentos, 128 partidas:

| regime no turno 144 | contextos | fita 0 | fita 1 |
|---|---:|---:|---:|
| sem `YARN_STORE` | 48 | **0,812** | 0,188 |
| com `YARN_STORE` | 16 | 0,000 | **0,125** |

A regra aponta para o lado certo nos dois regimes — e é por isso que forçar a fita 1 sem a
condição dela custa 0,624 de win rate. Um bloco não é uma peça de biblioteca: é uma resposta
a um mundo, e fora daquele mundo ele é um passivo.

## E o roteamento vale quanto, então

Nas **mesmas** seeds do painel (1070–1089) e contra os mesmos dois adversários:

| candidato | sem yarn | com yarn |
|---|---:|---:|
| fita 0 nua | 0,583 | 0,625 |
| fita 1 nua | 0,417 | 0,250 |
| **roteador completo** (`y_bare`, `y_lead_only`) | **0,750** | **0,750** |

O roteador vale **+0,167 e +0,125** sobre a melhor fita fixa, nas mesmas partidas. É onde o
valor da biblioteca já está, e a biblioteca não tem bloco melhor para dar: os 21 doadores
são as únicas alternativas que ela contém, e nenhuma vence.

## Um defeito de bancada descoberto no caminho

`thomas_t95` e `aberatozer_d5e3` concordaram no resultado em **80 de 80 contextos**, com
margens diferindo em 40 a 140 moedas. Faz sentido — o `d5e3` é um chassis reativo sobre as
mesmas fitas do `thomas95` —, mas a consequência é séria: uma busca que usa os dois como
coorte forte está usando **um adversário só**, e o critério de "pior oponente" do
`fitness` fica degenerado. As nove buscas acima continuam válidas como negativas, porque o
titular nunca foi batido, mas a diversidade era metade do que parecia.

O painel da issue #35 dá a saída: `yamakawanin_king_v4e` discordou dessas famílias no painel
novo e é a segunda família forte genuinamente distinta.

> **Complemento (mesmo dia).** A leitura de que "com yarn a biblioteca é fraca" vale para
> a fita **nua**. Com o segundo estágio ligado, o `v004` faz 0,792 nesse regime, e a
> ablação pareada dos dois estágios está em [ROUTING_ABLATION.md](ROUTING_ABLATION.md).

## O que a #39 decide agora

1. **O passo 1 está respondido, e é não.** Blocos e sufixos da mesma procedência não são
   intercambiáveis a partir de uma fronteira idêntica. A biblioteca do `yhay` foi enumerada
   por inteiro nas fronteiras onde ela tem alternativa.
2. **O passo 4 já está feito e é o que sustenta o número.** O roteador vale +0,125 a +0,167
   sobre a melhor fita fixa; refiná-lo sobre esta biblioteca não tem material novo para usar.
3. **Sobra construir fita nova, e agora com alvo.** O regime `com YARN_STORE` é onde a
   biblioteca inteira é fraca: a melhor fita nua faz 0,625 e a alternativa condicional faz
   0,250. É ali que um bloco novo teria valor, e é ali que o solver deve gastar partida.
4. **Antes disso, consertar a bancada**: trocar `aberatozer_d5e3` por `yamakawanin_king_v4e`
   como segunda família forte, senão toda busca futura otimiza contra um adversário só.

Nenhuma submissão, nenhuma seed de validação ou holdout consumida, `release_status` sempre
`not_validated`. Planos, hashes de gerador, histórico por doador e as 288 partidas de
auditoria em [block-swap.json](block-swap.json).

## Reprodução

```bash
# troca de bloco
python -m experiments.block_solver --mutation-space swap \
  --source opponents/public/yhay_router_0908/actions.json --tape-index 0 \
  --start 144 --days 6 --proposals 3 --rounds 1 \
  --opponents clock::opponents/public/thomas_t95/main.py,clock::opponents/public/aberatozer_d5e3/main.py \
  --seeds 1054:1058 --check-seeds 1058:1062 --workers 4 \
  --output experiments/searches/swap-144-01

# compromisso de sufixo, mesma fronteira e mesmas seeds
python -m experiments.block_solver --mutation-space swap ... --days full \
  --output experiments/searches/suffix-144-01
```
