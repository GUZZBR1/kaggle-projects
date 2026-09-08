# O topo público não roteia melhor: ele tem fitas melhores

Medição de 2026-09-08 do `yhay81/shop-router-0908` (rating 2713,9, 44º de 8177),
fixado em `opponents/public/yhay_router_0908`. 20 seeds `dev` (`1070:1090`), dois
assentos, 240 partidas, zero falhas.

| adversário | score do `yhay_router_0908` | margem média |
|---|---:|---:|
| `thomas_t95` | **0,750** | +2 729 |
| `v003` (nosso) | 0,800 | +9 032 |
| `thomas_t93` | 0,950 | +4 825 |
| `kaitofukami_v48` | 1,000 | +21 460 |
| `boatlee_v21` | 1,000 | +27 852 |
| `cok_v10` | 1,000 | +28 621 |
| **agregado (5 famílias públicas)** | **0,940** | — |
| **pior família** | **0,750** | — |

Para comparar com `docs/CHASSIS_FINDING.md`, que usou as mesmas seeds e as mesmas
cinco famílias:

| candidato | agregado | pior família | vs `thomas_t95` |
|---|---:|---:|---:|
| `yhay_router_0908` | 0,940 | 0,750 | 0,750 |
| `v23` (chassis sobre as fitas do thomas95) | 0,920 | 0,800 | 0,800 |
| `v003` (nosso portfólio roteado) | 0,695 | 0,325 | 0,325 |

Dois artefatos de arquiteturas opostas empatam no topo, e ambos passam do
`thomas_t95`.

## O que ele muda

O `main.py` é um roteador de fitas **puro**: nenhuma camada reativa, nenhum
conserto por turno. Ele carrega quatro fitas completas de 719 ações e um
`model.json` com duas decisões:

| passo | feature | teste | escolha |
|---:|---|---|---|
| 144 | `shop_count_7` (`YARN_STORE` revelado) | `<= 0,5` | fita 0, senão fita 1 |
| 648 | `market_stock_5` (estoque de `EGG` no mercado) | `<= 9888` | fita 2, senão fita 3 |

A estrutura das fitas revela o que cada decisão significa:

- fitas 0 e 1 compartilham 168 passos e divergem em 477 — a decisão do passo 144
  é uma **troca de plano de temporada inteira**;
- fitas 0 e 2 compartilham 649 passos e divergem em 21; fitas 0 e 3 compartilham
  672 e divergem em **2** — a decisão do passo 648 é uma **liquidação terminal**,
  não uma estratégia.

Ou seja: uma decisão grande no dia 6 e um ajuste de encerramento no dia 27. É um
roteador *mais simples* que o do `thomas_t95` (que ramifica em 2 de 10 blocos
lendo tiles e dinheiro do rival) e mais simples que a nossa própria ambição de
roteamento fino. Ele também é estritamente próprio: nenhuma feature usa o
oponente, o assento, a seed ou lojas futuras.

## De onde vem a força, então

Do `observation.py` que vem no mesmo bundle: ele é o entrypoint `ctypes` de uma
política nativa compilada, `hybrid_shopforge_3day_frontier_state_router_r5`, ABI 2
("ShopForge SixDay Guard"). O `agent.so` não é distribuído, e o roteador só usa
dele o empacotamento da observação. **As quatro fitas são a saída do solver
próprio do autor**, congelada — não fitas colhidas do replay de outra pessoa.

Os notebooks anteriores dele descrevem o método, e ele é explícito sobre o
limite: "public tapes are a teacher, not the final asset". A linha é:

1. baixar o top-200 e replays antigos, deduplicar histórias completas por SHA-256;
2. cortar nas fronteiras de loja e tratar blocos de 3 ou 6 dias como candidatos
   permutáveis;
3. testar candidatos **na mesma fronteira**, em seeds novas e nos dois assentos,
   em vez de comparar jogos inteiros não relacionados;
4. reter poucas rotas distintas e ajustar árvores minúsculas sobre features
   públicas;
5. depois, **gerar os próprios blocos** e pontuar o estado final de cada um
   (dinheiro, posição, inventário) para que ele conecte limpo no bloco seguinte.

O `Six-Day Public-State Fieldbook` dele reporta 0,955 de taxa de pontos em 27 520
partidas contra 215 oponentes em 64 seeds não usadas, com apenas seis rotas.

## O que isso corrige na nossa leitura

O `CHASSIS_FINDING` concluiu que a alavanca era o chassis reativo, porque com
fitas idênticas o chassis valia +0,225 de pior família sobre o roteamento. Isso
continua verdadeiro *com fitas idênticas*. O `yhay_router_0908` mostra o terceiro
eixo, e ele é maior que os dois: **sem nenhum chassis e com um roteador mais
simples que o nosso, fitas melhores chegam a 0,750 de pior família onde as nossas
chegam a 0,325.**

A ordem das alavancas, medida em pior família na mesma bancada:

| alavanca | ganho medido |
|---|---:|
| qualidade da fita (solver próprio vs. colheita) | +0,425 (0,325 → 0,750) |
| chassis reativo sobre as mesmas fitas | +0,225 (0,325 → 0,800) |
| roteamento sobre a melhor fita única | +0,150 (0,100 → 0,250) |

Nós pegamos a menor das três.

## Direção

O ponto 3 do método dele é o que nos falta e é barato: nossa arena já roda
comparação pareada em seeds novas nos dois assentos, mas comparamos **agentes
inteiros**. Comparar *blocos na mesma fronteira*, com o estado de chegada
pontuado, é o que transforma um dump de replays em biblioteca própria — e é
pré-requisito para qualquer solver nosso.

Duas frentes, nessa ordem:

1. **Splicing avaliado por bloco.** Cortar as fitas que já temos nas fronteiras de
   loja, medir cada bloco candidato a partir do mesmo estado, e manter os que
   chegam com dinheiro, posição e inventário conectáveis. `experiments/` já faz
   busca de sufixo; falta a pontuação do estado de chegada.
2. **Chassis sobre a melhor biblioteca resultante.** As oito camadas do `v23`
   continuam valendo, e continuam mensuráveis uma a uma — mas aplicadas a fitas de
   0,325 elas rendem menos do que aplicadas a fitas de 0,750.

O `yhay_router_0908` fica fixado como adversário de bancada: ele é hoje o teto
medido do campo público na nossa arena, no lugar do `thomas_t95`.

---

> **Atualização (2026-09-08).** O `yhay_router_0908` deixou de ser o teto medido:
> `versions/v004` reproduz o roteador dele exatamente e acrescenta uma única camada
> reativa, e vence o confronto direto por 0,960 em seeds de validação reservadas.
> Ver `docs/V004_ONE_LAYER.md`.
>
> Duas frentes que este documento propôs foram medidas e não pagam. Emendar as
> fitas do `thomas_t95` na abertura do yhay dá 0,000 em quatro das cinco. E o
> oráculo sobre as quatro fitas do yhay é 0,700 contra o `thomas_t95` onde a melhor
> fita sozinha já faz 0,650, com empate entre todas as fitas em 49 de 80 contextos:
> o roteamento sobre esta biblioteca está esgotado. Resta o ponto 5 do método dele,
> gerar blocos próprios.
