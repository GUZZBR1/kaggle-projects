# Os dois estágios sustentam tudo, e o mecanismo não é o nosso dinheiro

Passo 4 da #39, medido pelo nosso próprio protocolo pareado em vez de herdado por fé. As
duas regras de roteamento que o `v004` traz do `yhay81` foram removidas uma de cada vez e
comparadas contra o `v004` nas mesmas seeds, adversários e assentos.

Coorte corrigida conforme o `BLOCK_SWAP.md`: `thomas_t95` e **`yamakawanin_king_v4e`**, que
é uma família genuinamente distinta — o `aberatozer_d5e3` concordava com o `thomas_t95` em
80 de 80 contextos e não servia como segundo oponente.

## As duas ablações

Seeds `dev` separadas por regime: 12 seeds com `YARN_STORE` aberto no turno 144, e 12 sem.
Dois adversários, dois assentos, 48 partidas por perna.

| variante | regime | win rate | delta pareado | CI95 |
|---|---|---:|---:|---|
| `v004` | com yarn | **0,792** | — | — |
| sem o estágio 1 (`YARN_STORE`→fita 1) | com yarn | 0,125 | **−0,667** | [−0,875, −0,458] |
| sem o estágio 2 (`EGG`→fita 2/3) | com yarn | 0,125 | **−0,667** | [−0,875, −0,458] |
| `v004` | sem yarn | **0,917** | — | — |
| sem o estágio 2 | sem yarn | 0,042 | **−0,875** | [−1,000, −0,750] |

O estágio 1 não dispara em mundos sem yarn, então lá as duas versões são o mesmo artefato.

Os dois estágios são **carga estrutural**. Nenhum é enfeite herdado: tirar qualquer um leva
o agente de ~0,8–0,9 para ~0,1. Isso também explica a leitura incompleta do
`BLOCK_SWAP.md`: a fita 1 **nua** faz 0,250 em mundos com yarn, mas a fita 1 **com o
estágio 2** faz 0,792. O valor não está em nenhuma fita, está no par.

## O mecanismo, que não é o que a gente supunha

O estágio 2 escolhe entre as fitas 2 e 3, que diferem da fita 0 em 21 e 2 turnos, todos
depois do turno 649. Vinte e um turnos valendo 0,875 de win rate exigem explicação. A
telemetria dá:

| | nosso dinheiro | dinheiro do rival |
|---|---:|---:|
| efeito do estágio 2, sem yarn | **+1 549** | **−15 880** |
| efeito do estágio 2, com yarn | **+3 702** | **−10 913** |

**Oitenta a noventa por cento do efeito está no dinheiro do rival, não no nosso.** A
liquidação terminal certa não enriquece a gente: ela **nega preço ao adversário**. O mercado
é compartilhado, e a ordem em que despejamos o galpão nas últimas horas decide o preço que
as vendas dele realizam.

O caso individual (seed 1002, contra `thomas_t95`) mostra o formato: com o estágio 2 fazemos
100 659 contra 96 431 e vencemos; sem ele fazemos **mais** dinheiro, 101 942, e perdemos,
porque o rival sobe para 115 421.

Isso reposiciona todo o eixo econômico do projeto. Até aqui as fitas foram tratadas como
economia da própria fazenda — plantar, colher, vender melhor. O maior efeito medido até hoje
num bloco de 21 turnos é **interação de mercado contra o adversário**.

## O que fecha e o que sobra da #39

Fecha o passo 4: o roteamento sobre esta biblioteca está medido e é o que sustenta o número.
Não há regra herdada aceita sem prova.

O passo 3, "buscar blocos que batam o titular a partir da mesma fronteira", está **esgotado
por busca local**: somando os espaços de mutação, foram 62 propostas medidas em treze
buscas — mercado, produção, trabalho ciente do estado, troca de bloco e compromisso de
sufixo — e **nenhuma** melhorou uma partida. Inclusive no regime mais fraco: a fita 1 sobre
seeds com yarn dá 0,000 de pior oponente, e 12 edições de mercado no bloco 144:288 não
moveram nada.

A conclusão honesta é que **editar localmente uma fita existente não produz uma fita nova**.
Gerar economia própria exige um planejador que construa blocos do zero contra o motor, com
o alvo agora localizado: **timing de mercado terminal contra o livro compartilhado**, que é
onde os 21 turnos de diferença já valem 0,875 de win rate.

Nenhuma submissão, nenhuma seed de validação ou holdout consumida. Evidência com hashes de
candidato, adversários, seeds e agregados em [routing-ablation.json](routing-ablation.json).

## Reprodução

```bash
python -m experiments.chassis_portfolio \
  --tapes opponents/public/yhay_router_0908/actions.json \
  --stages '[[648,"market_inventory","EGG",9888,3,2]]' \
  --settings '{"sell_lead": true}' --output /tmp/v004-no-yarn/main.py

python -m arena.league --candidate clock::versions/v004/main.py \
  --paired-with clock::/tmp/v004-no-yarn/main.py \
  --opponents clock::opponents/public/thomas_t95/main.py,clock::opponents/public/yamakawanin_king_v4e/main.py \
  --seeds 1000,1001,1004,1006,1007,1011,1022,1024,1027,1028,1034,1049 \
  --split dev --workers 6 --output experiments/results/yarn-v004
# e a perna espelhada, depois:
python -m eval.ladder experiments/results/yarn-v004 experiments/results/yarn-v004-no-yarn
```
