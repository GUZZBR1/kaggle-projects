# As derrotas do v004 não são empates apertados: são derrotas de economia

Triagem de 2026-09-08, feita para decidir se vale atacar timing de venda e
liquidação terminal antes da issue #39. **Não vale.** O teto dessa alavanca no
painel atual é de duas partidas em 280.

## O que foi medido

`experiments/results/y_lead_only-panel/matches.csv` — o candidato que virou o
`v004`, split `dev`, seeds 1070–1089, sete famílias públicas, dois assentos,
280 partidas, backend `fast`. A margem por partida já é gravada por
`arena/match.py`, então a triagem é uma leitura do CSV existente e não uma
rodada nova.

| recorte | v004 (`y_lead_only`) | yhay sem a camada (`y_bare`) |
|---|---:|---:|
| partidas | 280 | 280 |
| derrotas | 22 | 24 |
| empates | **0** | **36** |
| derrotas com margem até 50 | **2** | 0 |
| derrotas entre 50 e 500 | 4 | 6 |
| derrotas entre 500 e 2 000 | 0 | 4 |
| derrotas entre 2 000 e 10 000 | **16** | 14 |

Derrotas por família, em ambos: `thomas_t95` 10, `aberatozer_v23` 10,
`thomas_t93` 2. O `y_bare` perde mais duas no espelho com o `yhay_router_0908`;
o `v004` não perde nenhuma.

## Leitura

**O regime de desempate já foi colhido.** Os 36 empates e as 2 derrotas de
espelho do `y_bare` viraram 0 e 0 no `v004`. Foi exatamente isso que o
`sell_lead` comprou, e é o que `V004_ONE_LAYER.md` mede como 0,960 no confronto
direto com o doador. A janela de "partida quase empatada decidida por timing de
mercado" existia, foi identificada e foi fechada.

**O que sobrou não é apertado.** Das 22 derrotas restantes, 16 passam de
2 000 moedas e apenas 2 ficam dentro de 50. Ganhar as duas move a win rate de
0,9214 para 0,9286: +0,007, dentro do ruído do bloco pareado, e portanto abaixo
do que o gate de `PAIRED_EVALUATION.md` promove. Nenhuma quantidade de precisão
em ordem de venda transforma uma derrota de 10 000 moedas em vitória.

**As duas famílias que nos batem nos batem por economia.** `thomas_t95` e
`aberatozer_v23` concentram 20 das 22 derrotas, e a distribuição delas é larga.
Isso é o gargalo de biblioteca que `V004_ONE_LAYER.md` já tinha localizado por
outro caminho — o oráculo sobre as quatro fitas do yhay é 0,700 contra o
`thomas_t95` enquanto a melhor fita sozinha já faz 0,650 — e é o que a issue #39
existe para atacar.

## Consequência

A ordem das alavancas não muda. Timing de mercado e liquidação terminal são
alavancas de desempate, e o desempate já está ganho no painel que medimos. A
alavanca aberta continua sendo gerar fitas próprias com solver próprio.

A camada `terminal_liquidation` do chassis, medida inerte nas três famílias da
ablação de `V004_ONE_LAYER.md`, é inerte pelo mesmo motivo: as fitas do yhay já
liquidam. O que decide a liquidação nelas é a *ordem dos slots de venda*, que as
variantes terminais das fitas 2 e 3 já resolvem, e restringir esse estágio piora.

Esta triagem é reprodutível a partir dos CSVs versionados; nenhuma partida nova
foi rodada para produzi-la.
