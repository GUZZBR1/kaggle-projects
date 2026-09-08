# Uma camada paga, uma camada mata, e seis não fazem nada

Medição de 2026-09-08. O `v004` é a primeira submissão nossa que bate o teto do
campo público em vez de perder para ele, e o ganho inteiro vem de uma decisão de
uma linha, tomada com base em ablação e não em fé.

## O ponto de partida

`docs/YHAY_ROUTER_FINDING.md` já tinha fixado o `yhay81/shop-router-0908` como o
melhor artefato público que medimos, e `docs/CHASSIS_FINDING.md` tinha medido o
chassis reativo do `ahmedberatozer` valendo +0,225 de pior família sobre fitas
idênticas. A hipótese óbvia era somar os dois: as melhores fitas com o melhor
runtime.

Primeiro foi preciso reproduzir o roteador. `experiments/chassis_portfolio.py`
renderiza as quatro fitas do yhay com os dois estágios do `model.json` dele
traduzidos, e o resultado joga **exatamente** o mesmo jogo: contra `boatlee_v21`,
`cok_v10`, `kaitofukami_v48`, `thomas_t93` e `thomas_t95` as margens médias batem
dígito a dígito (27 852 / 28 621 / 21 460 / 4 825 / 2 729), e no espelho contra o
próprio yhay dá 0,500 com margem zero em 40 partidas. A partir daí qualquer
diferença medida é uma diferença nossa, não ruído de reimplementação.

## O chassis inteiro é catastrófico nessas fitas

| candidato | agregado | vs thomas95 | vs yhay | ações de unidade ineficazes |
|---|---:|---:|---:|---:|
| fitas do yhay, sem camadas | 0,850 | 0,750 | 0,500 | 12 641 |
| fitas do yhay, chassis completo | **0,300** | 0,000 | 0,000 | **92 972** |

Perde 13 mil moedas para tudo. O chassis não é ruim — ele é o runtime de um
artefato que mede 0,808 agregado. Ele é ruim *nessas* fitas.

## Ablação: qual camada

Cada camada ligada sozinha, 120 partidas contra `thomas_t95`, `thomas_t93` e
`aberatozer_v23`, dois assentos, 20 seeds `dev`.

| camada | vs thomas95 | vs thomas93 | vs v23 |
|---|---|---|---|
| nenhuma | 0,700 / +2 636 | 0,875 / +4 361 | 0,800 / +2 775 |
| **`budget_guard`** | **0,000 / −17 227** | **0,000 / −15 298** | **0,000 / −17 016** |
| **`sell_lead`** | **0,750 / +3 895** | 0,875 / **+6 010** | 0,750 / +3 921 |
| `weed_repair` | 0,700 / +2 550 | 0,900 / +4 302 | 0,800 / +2 690 |
| `hand_align`, `clamp_sells`, `dead_stock`, `room_guard`, `terminal_liquidation` | inertes | inertes | inertes |

**O `budget_guard` sozinho explica o colapso inteiro.** Ele financia as compras de
cada bloco vendendo estoque, e as fitas do yhay rodam sobre arbitragem de mercado:
elas compram e revendem o mesmo produto no mesmo turno, contando com um caixa que
o guard drena. As outras sete camadas somadas não chegam perto desse efeito.

Isso também corrige a leitura do `CHASSIS_FINDING`. O chassis não é um conserto
genérico de fitas replayadas; ele é um conjunto de camadas afinadas para a economia
das fitas do `thomas_t95`. Trocada a economia, a mesma camada que sustentava passa
a destruir.

## O `sell_lead`, de novo, e desta vez com valor real

`docs/SELL_LEAD_CORRECTION.md` retratou o `sell_lead` porque nas *nossas* fitas
ele só ganhava o desempate do espelho por uma moeda: elas vendem no instante em
que a mercadoria chega ao galpão, sem folga para antecipar. Nas fitas do yhay há
folga, e o efeito é de outra ordem de grandeza.

Validação pareada em 25 seeds do split `validation`, reservadas e nunca usadas,
sete famílias públicas, dois assentos, 350 partidas por perna:

| oponente | yhay sem a camada | **v004** |
|---|---:|---:|
| `thomas_t95` | 0,700 / +3 730 | **0,740 / +5 450** |
| `thomas_t93` | 0,840 / +4 743 | **0,860 / +6 554** |
| `aberatozer_v23` | 0,680 / +2 640 | **0,720 / +4 320** |
| `kaitofukami_v48` | 0,940 | 0,940 |
| `cok_v10` | 1,000 | 1,000 |
| `boatlee_v21` | 1,000 | 1,000 |
| **`yhay_router_0908`** | 0,500 (espelho) | **0,960 — 48/50, +2 059** |
| **agregado** | 0,809 | **0,889** |
| **pior família** | 0,680 | **0,720** |

Nenhum oponente piora, em placar ou em margem, fora da amostra. E o confronto
direto contra o doador não é desempate: são 2 059 moedas de margem média em 50
partidas, contra as 1 moeda que o `SELL_LEAD_CORRECTION` diagnosticou no caso
degenerado. O critério para distinguir os dois casos continua sendo o mesmo que
aquele documento estabeleceu — olhar a distribuição de margens antes de acreditar
no placar — e aqui ela sustenta o achado.

## Duas hipóteses que não sobreviveram

**O guard do estágio terminal.** As fitas 2 e 3 do yhay são variantes terminais da
fita 0 apenas: divergem dela a partir do passo 649 e 672, enquanto a fita 1 é um
plano de temporada diferente desde o passo 168. O estágio do passo 648 dispara
incondicionalmente, então um jogo que pegou o ramo do yarn store é emendado, nos
últimos três dias, num plano estranho ao estado que ele produziu. Restringir o
estágio à rota que ele varia **piora**: 0,700 contra o `thomas_t95` em vez de
0,750, 0,875 contra o `thomas_t93` em vez de 0,950, e 0,425 no confronto direto.
A emenda "ruim" custa menos do que ficar sem variante terminal nenhuma. O que
essas variantes decidem é a *ordem dos slots de venda* na liquidação final — o
motor resolve as ordens de mercado por índice entre os dois assentos, então quem
põe o item certo no slot certo pega o preço melhor. É uma corrida, e correr com a
ordem errada ainda é melhor do que não correr.

**Ampliar a biblioteca com as fitas do `thomas_t95`.** Nove fitas na mesma
fronteira, abertura normalizada para a do yhay, decisão no passo 144, 80 contextos
(20 seeds × 2 adversários × 2 assentos):

| fita | procedência | score médio |
|---|---|---:|
| `n_y3` | yhay | 0,550 |
| `n_y2` | yhay | 0,450 |
| `n_y0` | yhay | 0,400 |
| `n_y1` | yhay | 0,225 |
| `n_t1` | thomas95 | 0,175 |
| `n_t0`, `n_t2`, `n_t3`, `n_t4` | thomas95 | **0,000** |

As fitas do `thomas_t95` não transferem para a abertura do yhay, o que é
exatamente o que `docs/SPLICE_DISTANCE.md` prevê para emendas entre procedências
diferentes. E dentro das quatro fitas do yhay o oráculo contra o `thomas_t95` é
0,700 enquanto a melhor fita sozinha já faz 0,650: em 49 dos 80 contextos todas
as fitas empatam. **Não sobrou teto no roteador.** O gargalo é a biblioteca.

## O que isso diz sobre a direção

A ordem das alavancas que o `YHAY_ROUTER_FINDING` levantou continua de pé, e esta
medição fecha as duas de baixo. O roteamento sobre esta biblioteca está esgotado,
e o chassis reativo não é transferível entre economias. O que resta é a alavanca de
cima: **gerar fitas próprias com solver próprio**, que é o ponto 5 do método do
yhay e a única coisa que ainda separa o `v004` do topo real do ladder.

O `aberatozer_v23` também precisa ser reclassificado. O `CHASSIS_FINDING` o mediu
em 0,920 agregado e 0,800 de pior família, mas naquele painel não havia o yhay.
No painel completo ele faz 0,808 agregado e **0,250 de pior família**, perdendo
0,250 para o yhay. A melhor família dele naquela medição era o próprio doador.
