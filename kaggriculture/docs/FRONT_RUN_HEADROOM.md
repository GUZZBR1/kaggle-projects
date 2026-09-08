# O teto do front-run é medível, e hoje ele é 0,0071 — issue #41

O `docs/NEAR_TIE_TRIAGE.md` fez essa contagem uma vez, à mão, para decidir uma
prioridade. Esta issue transforma a contagem em instrumento — `eval/near_ties.py` —
porque o número não é uma propriedade do nosso agente: é uma propriedade da coorte
com quem o ladder nos pareia, e ela muda a cada `PANEL_REFRESH`.

## O que o instrumento mede

Para cada limiar de margem, quantas partidas o motor já decidiu dentro dele **e nós
não ganhamos**. Um empate já vale 0,5, então ele conta metade de uma derrota: tratar
os dois como iguais inflaria o teto exatamente no valor que o Bradley–Terry não paga.
A saída é o `headroom` — o ganho máximo de win rate se toda partida quase decidida
virasse vitória — quebrada por oponente e **por assento**, porque a corrida de mercado
é resolvida por índice de ordem entre os dois assentos e uma camada que só paga de um
lado é um achado diferente de uma que paga dos dois.

## O instrumento se valida sozinho

Aplicado aos dois painéis já versionados, com o mesmo comando:

| painel | win rate | headroom (50) | teto | veredito |
|---|---:|---:|---:|---|
| `y_bare` (antes do `sell_lead`) | 0,8500 | **0,0643** | 0,9143 | **construir** |
| `y_lead_only` (v004) | 0,9214 | **0,0071** | 0,9286 | **não construir** |

No painel anterior, o headroom inteiro está concentrado em um único oponente — o
espelho `yhay_router_0908`, com **0,45** — e são 36 empates, zero derrotas. Ou seja: o
instrumento redescobre sozinho, sem ser informado de nada, a janela exata que o
`sell_lead` explorou, e a mede como grande. No painel de hoje ela mede 0,0071, com as
duas derrotas restantes contra o `aberatozer_v23`.

Isso é o que dá crédito ao veredito negativo. Um medidor que só sabe dizer "não" não
seria evidência de nada.

## A barra

O padrão é 0,02 de win rate. Abaixo disso o efeito não produz o CI95 estritamente
positivo que o `eval/submit_gate.py` exige sobre 100 blocos pareados, então a camada
seria infalsificável justamente na única medição que promove alguma coisa. Com 0,0071
o teto perfeito do front-run está três vezes abaixo da barra.

A banda de 500 moedas dá 0,0214, marginalmente acima da barra, e **não deve ser lida
como alcançável**: 500 moedas não é um desempate de timing de venda, é diferença
econômica. O limiar honesto para uma camada de mercado é o de 50.

## Decisão

Os passos 2 a 4 da issue #41 — fingerprint de oponente, front-run condicional e o
gate — **não são construídos agora**. O passo 1 fica versionado e roda junto do
refresh de painel; se a coorte convergir para famílias irmãs da nossa, o headroom
sobe sozinho e a issue reabre com número, não com intuição.

```
.venv/bin/python -m eval.near_ties experiments/results/<run> --bar 0.02
```

O precedente que justifica esse cuidado é o `SELL_LEAD_CORRECTION.md`: uma camada de
venda que parecia carregar o resultado inteiro e era desempate de espelho por uma
moeda. A diferença entre aquele caso e o `V004_ONE_LAYER.md` foi sempre olhar a
distribuição das margens antes de acreditar no placar. Isso agora é um comando.
