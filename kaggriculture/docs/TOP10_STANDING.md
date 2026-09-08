# O número principal do harness passa a ser win rate contra o topo, não rating

O prêmio do Kaggriculture é um degrau, não uma rampa: da 1ª à 10ª posição paga-se
US$ 5.000 em cada, e a 11ª paga o mesmo que a 100ª. Então a pergunta que o harness
precisa responder deixou de ser "o candidato melhorou" e passou a ser "ele é forte o
bastante, em termos absolutos, contra o topo". São estatísticas diferentes: a primeira
é o delta pareado do `eval/ladder.py`, que continua sendo o teste de promoção entre
dois agentes **nossos**; a segunda é o `eval/standing.py`.

## Por que rating não é o KPI

Rating não aparece neste relatório, de propósito. Ele atrasa, depende da idade e da
trajetória da submissão, o Bradley–Terry final o descarta como critério fundamental, e
os agentes mais fortes estão sendo retirados do ladder — então o melhor oponente
observável não é o melhor oponente existente. Win rate absoluto contra um painel que
nós controlamos sobrevive aos quatro problemas. Gold, pelo mesmo motivo do
`LADDER_OBJECTIVE.md`, não entra nem como fitness nem como manchete.

## As faixas

O corte único de rating não serve aqui: um candidato que atropela os ranks 30–100 e
apenas empata com o top 10 não é candidato a top 10. As barras são por faixa de
posição:

| faixa | barra |
|---|---:|
| `top10` | 55% |
| `rank10_30` | 60% |
| `rank30_100` | 65% |

Uma faixa **vazia é "unmeasured", nunca "pass"**. Um oponente sem rank conhecido cai em
`unbanded`, é reportado e não decide nada — a mesma disciplina do `ratings.json`, onde
ausente, velho e desconhecido caem para fora da coorte forte e nunca para dentro.

## Os dois níveis

- **`promotion gate = PASS`** — toda faixa povoada acima da sua barra, e nenhuma
  lineage nos segurando abaixo do piso de 40%. O piso existe porque um 25–75 estrutural
  contra uma lineage comum afunda a corrida por mais bem que o agregado leia.
- **`defended standing = YES`** — além do acima, win rate contra o top 20 ≥ 58% com o
  limite inferior do CI claramente acima de 50%. É o ponto em que a equipe deixa de
  tentar entrar no top 10 e passa a disputá-lo.

Assento e pior lineage não são enfeite: um candidato carregado por um assento, ou que
desaba contra uma única lineage comum, é exatamente o modo de falha que o agregado
esconde.

## O que a primeira execução revelou

Rodado sobre o painel público atual com o `v004`:

```
WR = 92.1%   95% CI = [86.4%, 97.1%]   (280 games, 20 seed blocks)
seat0 = 92.1%   seat1 = 92.1%
worst lineage = 75.0% (aberatozer_v23)   median lineage = 100.0%

  top10        unmeasured  need 55%  FAIL  (0 games)
  rank10_30    unmeasured  need 60%  FAIL  (0 games)
  rank30_100       100.0%  need 65%  PASS  (40 games)

promotion gate = FAIL
```

92,1% contra o painel, e **o gate reprova mesmo assim** — corretamente. O melhor
artefato público que conseguimos fixar é o `yhay_router_0908`, rank 45 por limite
superior do time autor. **Não existe hoje no painel um só oponente do top 30.** As duas
faixas que decidem a briga estão vazias, e um agregado de 92% contra o que sobrou não é
evidência de nada sobre o top 10.

Esse é o achado que o relatório existe para tornar impossível de ignorar: o gargalo
imediato não é a força do agente, é que **não temos com quem medir**. O teto do painel
público está no rank 45 e os agentes fortes estão escondidos; a única fonte de
adversários do topo real é o dataset diário de replays de episódios mais bem
classificados (`kaggle/kaggriculture-episodes-index`), que o `LADDER_META.md` já
documenta e que o `experiments/tape_agent.py` já sabe reproduzir.

```
.venv/bin/python -m eval.standing experiments/results/<run> --ranks ranks.json --candidate v004
```
