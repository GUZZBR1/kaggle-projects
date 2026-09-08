# O objetivo local passa a ser o objetivo do leaderboard

Fecha as issues #31 e #33. O que estava errado até aqui não era a arena — era o que a
arena otimizava.

## O que estava errado

O leaderboard é um ajuste de Bradley-Terry sobre episódios, e um episódio contribui com
vitória, derrota ou empate. **Margem de moedas não entra.** Nossa seleção reportava e
argumentava com margem, então uma mudança que ganha as mesmas partidas com folga maior
parecia progresso e não valia nada no ladder.

O `v004` é o caso concreto. Refeita a comparação pareada e bloqueada por seed:

| recorte | v004 | yhay | delta | CI95 |
|---|---:|---:|---:|---|
| painel completo | 0,8886 | 0,8086 | +0,080 | [+0,044, +0,116] |
| **sem o espelho com o yhay** | 0,8767 | 0,8600 | **+0,017** | **[−0,030, +0,063]** |
| só contra `yhay_router_0908` | 0,9600 | 0,5000 | +0,460 | [+0,406, +0,514] |

As margens melhoraram de 1 200 a 1 600 moedas em todas as famílias. Foi nisso que a
submissão foi gasta.

## O segundo problema: o pareamento é adaptativo

Um agente perto do topo para de ser pareado com a ponta fraca do painel. Contra
`cok_v10` e `boatlee_v21` fazemos 1,000, e assim que estivermos em 2 700 essas partidas
deixam de existir. Um agregado que faz a média incluindo elas é um número que o ladder
nunca vai reproduzir.

## O que `eval/ladder.py` faz

- **Métrica primária: `win_rate_strong`**, sobre a coorte com rating datado acima do corte
  (2 300 por padrão, parametrizável).
- **Métrica secundária: `win_rate_all`**, sobre o painel inteiro. Os fracos não são
  descartados: o ajuste final roda sobre os agentes que continuarem ativos, não sobre um
  corte formal de rating, e um candidato que desaba contra uma família fraca continua sendo
  um candidato com um buraco.
- **W/L/T explícito** por oponente. Empate vale 0,5, como no BT. Uma pontuação que não seja
  1, 0,5 ou 0 levanta erro — é a guarda contra alguém passar margem como score.
- **Margem vira diagnóstico**, com o nome dizendo isso (`mean_margin_diagnostic`). Ela
  continua servindo para distinguir efeito real de desempate de espelho de uma moeda, que é
  o que o `SELL_LEAD_CORRECTION` ensinou, e é só para isso que ela serve.
- **Rating ausente ou velho cai fora da coorte forte**, nunca dentro. Um rating que
  envelheceu é o mesmo que rating nenhum, e deixar um oponente não medido entrar por omissão
  decidiria em silêncio justamente o que a métrica primária existe para medir. O limite de
  idade é de 14 dias. `opponents/ratings.json` guarda só observações diretas; a issue #32
  preenche o resto e documenta o refresh.

## Comparação pareada

Os dois lados enfrentam os mesmos adversários nas mesmas seeds e nos mesmos assentos, então
os placares são fortemente correlacionados e um CI construído a partir de duas win rates
independentes é largo demais. A estatística é a **diferença por bloco**, e a unidade de
reamostragem é o bloco de seed, não a partida. Uma comparação que não esteja perfeitamente
pareada levanta erro em vez de alargar o intervalo em silêncio.

Isso não fabrica sinal. Se o efeito verdadeiro for perto de zero, mais blocos compram um
intervalo mais apertado em torno de zero — que é exatamente a resposta que se quer antes de
gastar uma submissão.

## O diagnóstico que faltava no desenho do gate

Regressão concentrada já estava previsto: um ganho comprado perdendo para os dois agentes
mais próximos do topo não é ganho. Mas o caso do `v004` é o simétrico, e é mais insidioso —
**concentração de ganho**. `leave_one_out` recalcula o delta primário deixando cada oponente
forte de fora por vez, e `carried_by` nomeia aqueles cuja remoção deixa o delta
indistinguível de zero:

```
primary  delta_win=+0.2500 CI95=[+0.1900,+0.3100]  n=100
  sem thomas_t95           delta=+0.4600 CI=[+0.4000,+0.5000]
  sem yhay_router_0908     delta=+0.0400 CI=[-0.0800,+0.1600]
carried_by: ['yhay_router_0908']
```

O ganho inteiro é de um oponente só. Um espelho contra o artefato de quem herdamos as fitas
carrega o número agregado enquanto o candidato é indistinguível do titular contra todo o
resto. Com esse diagnóstico no lugar, o `v004` teria recebido **NO SUBMIT**.

## Como usar

```
python -m eval.ladder <dir-do-titular> <dir-do-candidato> [--cut 2300] [--output x.json]
```

A issue #36 transforma isso em veredito. A #34 monta o driver de 100 blocos pareados que
alimenta o número com resolução suficiente para o gate significar alguma coisa.
