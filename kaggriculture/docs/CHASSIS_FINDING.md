# O ganho não está no roteador, está no chassis reativo

Medição de 2026-09-08, 200 partidas por candidato: 20 seeds `dev` (`1070:1090`),
cinco famílias fixadas, dois assentos, zero falhas.

| candidato | agregado | **pior família** | vs thomas_t95 | vs thomas_t93 |
|---|---:|---:|---:|---:|
| **v23** (chassis + fitas do thomas95) | **0,920** | **0,800** | **0,800** | **0,800** |
| `v003` (nosso portfolio de 2 fitas) | 0,695 | 0,325 | 0,325 | 0,400 |

O v23 **vence o `thomas95`**, que era o teto do campo em toda medição anterior
nossa. Nosso `v003` perde para ele. A diferença de pior família é 0,800 contra
0,325.

## O que o v23 faz de diferente

Ele não é um roteador melhor. Ele usa **as mesmas cinco fitas do `thomas95`** —
verifiquei reconstruindo o artefato a partir do nosso `opponents/public/thomas_t95`
e do chassis extraído do notebook (SHA-256 confere com o declarado). O que muda é
que a fita deixa de ser a ação final e passa a ser um *plano*, corrigido a cada
turno por camadas reativas:

| camada | o que corrige |
|---|---|
| `hand_align` | ajusta ações de mão ao número real de mãos |
| `weed_repair` | escava um weed que bloqueia PLANT/BUILD e replica |
| `sell_lead` | vende os lotes do próximo passo um passo antes |
| `budget_guard` | financia as compras de cada bloco de 72 turnos |
| `room_guard` | mantém o galpão ≤ 99 na hora 23 |
| `clamp_sells` | apara ordens SELL ao galpão projetado |
| `dead_stock` | vende estoque que a rota nunca venderia |
| `terminal_liquidation` | no passo ≥ 718 liquida o galpão projetado |

## Por que isso importa mais do que parecia

O `LADDER_META.md` já tinha encontrado a peça central: *"um fluxo gravado só é um
agente forte se o agente que o produziu não estava se adaptando... Replicado numa
cidade com um mix de shops diferente, o plano simplesmente está errado."* Foi por
isso que 1 311 das 1 313 fitas do dump fizeram 0,00.

**O chassis é exatamente o conserto disso.** Ele não escolhe uma fita melhor para
o mundo — ele conserta a fita *para* o mundo, turno a turno. É por isso que ganha
0,225 de pior família sobre o nosso portfolio usando fitas idênticas às do
agente que ele supera.

Nosso `v003` investiu no eixo errado. O roteamento vale (o próprio `LADDER_META`
mediu +0,08 agregado), mas é a menor das duas alavancas, e nós pegamos só ela.

## Direção

Construir um chassis reativo nosso sobre as fitas que já temos, e só depois voltar
ao roteador. As camadas são independentes e chaveáveis, então cada uma pode ser
medida isoladamente com o protocolo pareado que já existe — que é como se
descobre quais delas realmente pagam, em vez de adotar as oito por fé.

O `terminal_liquidation` e o `dead_stock` são os primeiros candidatos: nossa
telemetria diária já reporta `unsold_items` e sobra de galpão, então o ganho é
mensurável antes mesmo de implementar.
