# O valor não está na fita, está no roteamento

Experimento para responder se dá para superar o topo público. Hipótese testada
e **rejeitada**, o que localiza onde o ganho realmente está.

## A hipótese

O artefato mais forte medido (`thomastschinkel 95.5%`) carrega 5 fitas de ação
e ramifica em apenas 2 dos seus 10 blocos de decisão. A colheita mostrou que
ele emite só **3 fluxos de ação distintos em 24 partidas vencidas** variadas.
Parecia quase open-loop. Se o roteamento faz tão pouco, talvez tocar apenas a
melhor fita fosse igual ou melhor — e mais simples.

## O resultado

Construímos um replayer da melhor fita colhida (margem +37.246, colhida de uma
vitória do `thomas 93.8`) e medimos em 21 seeds, dois assentos, 168 partidas.

| adversário | score da fita única | margem |
|---|---:|---:|
| thomastschinkel 95.5% | **0,050** | −8.747 |
| thomastschinkel 93.8% | **0,150** | −6.662 |
| boatlee V16-RC5 | 0,875 | +12.377 |
| cok_v10 | 0,950 | +16.648 |
| **agregado** | **0,506** | +3.404 |

Contra os agentes de onde a fita veio, ela perde. Contra os mais fracos, vence.
O `thomas 95.5` faz 1,000 contra as mesmas famílias públicas; a fita dele
sozinha faz 0,506.

## A leitura, que contradiz a aparência

As fitas são **específicas de confronto**. Uma fita que venceu o `cok_v10` não
vence o `thomas 95.5`. Os 3 fluxos distintos não significam que o roteamento é
inútil — significam que, contra aqueles adversários, ele convergia para poucas
respostas. Contra adversários diferentes ele escolhe diferente, e é exatamente
essa escolha que produz a vitória.

Isso é coerente com o vetor público que eles alimentam na árvore: ele inclui
**população de tiles do rival e dinheiro do rival**. O roteamento está lendo o
oponente, não só o próprio estado.

## Onde fica o ganho

O gargalo deles é a granularidade, não o conceito:

- ramificam em **2 de 10 blocos**; 8 blocos não decidem nada;
- carregam **5 fitas**, duas quase duplicadas;
- as árvores usam 2 e 1 teste de feature.

Nós temos o que falta para atacar isso: um colhedor que gera fitas rotuladas
pelo confronto e pela margem que produziram, e uma arena que seleciona por pior
família em vez de agregado. O caminho é biblioteca maior de fitas
**especializadas por confronto** mais roteamento mais fino sobre o estado do
rival — não uma fita melhor.

## Nota de método

O replayer de fita única fica no repositório como piso honesto de comparação:
comportamento fixo, zero adaptação. Qualquer coisa que a gente construir tem
que ganhar dele para justificar a complexidade. Ele passa no preflight com
91,5% de taxa de ação e streak ocioso de 2, contra 85,4% e 11 do `v002`.
