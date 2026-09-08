# O gate comparava com o teto do painel, não com o nosso próprio agente ativo — issue #40

O `v004` foi barrado pelo gate e, submetido mesmo assim, subiu a equipe de **2359,8
para 2551,4** e da posição **547 para a 243** entre 8206. As duas coisas estavam certas.
Elas respondiam perguntas diferentes, e o gate estava fazendo a errada.

## As duas comparações, agora rodadas lado a lado

O `PAIRED_EVALUATION.md` comparou o `v004` com o `y_bare` — nossa reprodução exata do
`yhay_router_0908`, o artefato mais forte do painel. Faltava a comparação que uma decisão
de submissão realmente faz: contra o **`thomas_t95`**, o agente que ocupava nosso slot
ativo. Rodada agora, mesmo painel de sete famílias, dev, seeds 1070–1089, dois assentos,
560 partidas (`docs/incumbent-t95-comparison.json`):

| | vs incumbente (`thomas_t95`) | vs teto do painel (`y_bare`) |
|---|---:|---:|
| coorte forte | **+0,500** — CI95 [+0,300, +0,650] | +0,080 — CI95 [+0,046, +0,114] |
| painel inteiro | **+0,243** — CI95 [+0,164, +0,314] | +0,080 |
| sem o espelho | — | **+0,017** — CI95 [−0,027, +0,060] |
| `carried_by` | **[]** | `yhay_router_0908` |
| pior oponente | **+0,000** (nenhuma regressão) | — |

Por oponente, contra o incumbente: `yhay_router_0908` +0,750, `aberatozer_v23` +0,550,
`thomas_t95` +0,250 no espelho, `thomas_t93` +0,150, e zero contra as três famílias que
ambos já ganham 1,000. O ganho não depende de nenhum adversário: `carried_by` é vazio,
o que é justamente o teste que a comparação contra o teto reprovava.

## O defeito

O gate lia a segunda coluna. Como o painel é construído a partir do topo público
*precisamente porque ele é mais forte que nós*, a linha de base quase nunca é o nosso
agente ativo — e um gate que exige superar o teto do painel bloqueia toda submissão que
de fato levanta a pontuação. Era o caso normal, não o excepcional.

## O que mudou em `eval/submit_gate.py`

`decide(comparison, incumbent=None, ceiling=None)`, `policy_version` 2.

- **O incumbente é declarado, e conferido por hash** contra o `baseline_hash` que o lote
  pareado congelou. O `arena/paired.py` deriva esse hash do próprio agente que vai rodar
  (`--incumbent-id`, `--displaces`), então uma declaração que nomeia o agente errado é
  pega pelo `check_spec`, não por confiança.
- **Recusa em vez de resposta.** Uma comparação cuja perna base não é o incumbente
  declarado devolve **`NO DECISION`**, com os dois hashes no texto. Medir distância até o
  topo público é útil e continua sendo emitido; não é autorização de release.
- **Uma medição que reprova continua `NO SUBMIT`**, com a recusa anexada. Amaciar para
  `NO DECISION` apagaria o achado, e nada fica autorizado de qualquer forma. É o caso
  *aprovado* contra um não-incumbente que precisa ser recusado.
- **`displaces` é obrigatório na declaração.** O item 1 do `FINAL_SUBMISSION_POLICY.md`
  exige identificar qual submissão ativa o envio destrói, e nenhum passo posterior
  consegue reconstruir isso. O texto do `SUBMIT` nomeia o histórico que se perde.
- **Os dois números viajam juntos.** `delta_over_baseline` decide; `delta_over_panel_ceiling`
  entra como diagnóstico marcado, e um teste garante que ele não muda o veredito.

O `PAIRED_EVALUATION.md` continua válido como medição: o `yhay_router_0908` é declarado
como base de medição, papel `measurement`, e o veredito que aquele run registrou —
`NO SUBMIT`, nomeando o espelho — não muda.

## Por que este run ainda diz `NO SUBMIT`, e por que não gastamos as seeds para mudar isso

O veredito contra o incumbente é `NO SUBMIT` por **duas razões, ambas de proveniência**:
split `dev` e 20 blocos pareados. Nenhum critério sobre o *efeito* reprova. Um `SUBMIT`
exigiria 100 blocos no split `validation`, e restam 75 seeds reservadas (100125–100200).

Não gastamos essas seeds, e a razão é substantiva, não de custo: **o incumbente mudou**.
O `v004` é o agente ativo hoje, avaliado em 2551,4. Uma corrida de 100 seeds de validação
provando que o `v004` supera o `thomas_t95` autorizaria retroativamente uma decisão já
tomada, e queimaria a reserva que o próximo candidato real precisa. O registro de seeds
existe para impedir exatamente esse tipo de consumo.

O gate está consertado e coberto por testes sobre a evidência real; o `SUBMIT` sai na
primeira comparação de release de verdade, com o `v004` declarado como incumbente.

## Nota lateral que a corrida expôs

Só `thomas_t95` e `yhay_router_0908` entraram na coorte forte. `aberatozer_v23`,
`cok_v10`, `kaitofukami_v48` e `thomas_t93` saíram como `unknown` — rating ausente ou
com mais de 14 dias, que o `LADDER_OBJECTIVE.md` manda tratar como rating nenhum. Isso
é o refresh da #32 vencendo, não um defeito do gate, mas estreita a coorte forte a duas
famílias, que é o mínimo que o próprio gate aceita.
