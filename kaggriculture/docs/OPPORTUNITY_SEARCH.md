# Trabalho legal não é o gargalo: os slots ociosos estão ociosos de propósito

Etapa 3 da #39, e a resposta à "próxima hipótese" que o
[PRODUCTION_SEARCH.md](PRODUCTION_SEARCH.md) deixou aberta: gerar trabalho sem olhar o
estado produz ação sem efeito, então o gerador precisa ler o alvo, a carga e os recursos.
Agora ele lê. **O resultado é que a legalidade não era o problema.**

## O que o gerador novo faz

`experiments/opportunity_mutations.py` propõe trabalho apenas onde a pré-condição do motor
já vale no tile em que a unidade está *naquele turno*:

| trabalho | pré-condição no motor (`kaggle_environments` 1.32.7) |
|---|---|
| `WATER` | tile é `PLANT` e `watered_today` é falso |
| `HARVEST` | `yield_units > 0` e, para planta, a idade passou de `first_yield_day` |
| `FERTILIZE` | tile é `PLANT` e a unidade carrega `FERTILIZER` |
| `FEED` | há animal colocado, `fed_today` falso e a unidade carrega `WHEAT` |
| `CARE` | há animal colocado e `cared_today` falso |
| `COLLECT_FERTILIZER` | há animal colocado e `fertilizer_available` verdadeiro |

Não existe modelo de mundo aqui: o motor é o modelo. O solver ganhou um `probe`, uma
partida cujo único fim é observar a trajetória do próprio titular dentro do bloco, com um
snapshot por turno. As oportunidades saem dessas observações reais — posição da unidade,
tile sob ela, inventário daquela unidade, dia corrente.

Dois cuidados, porque a leitura é da trajetória do titular:

- **Contexto.** Uma trajetória pertence a uma seed, assento e adversário. São dois probes
  por rodada e só o que **os dois** admitem vira proposta.
- **Auto-invalidação.** Aplicar várias oportunidades de uma vez pode invalidar as
  seguintes: uma segunda `WATER` no mesmo tile e dia é no-op pela mesma regra que autorizou
  a primeira. Duplicatas por (dia, tile, trabalho) colapsam no turno mais cedo, e o que
  sobra é medido, nunca suposto.

## A seletividade, que é o efeito imediato

| bloco | slots ociosos | oportunidades compartilhadas |
|---|---:|---:|
| 72:144 | 69 | **7** |
| 144:288 | 99 | **23** |
| 648:719 | 74 | **28** |

E o diagnóstico de ações sem efeito, que era o sintoma do gerador cego:

| gerador | ações sem efeito por perna de 16 partidas |
|---|---:|
| cego (`--mutation-space production`) | 1 696 – 1 800 |
| titular (referência) | 128 – 212 |
| **ciente do estado (`--mutation-space opportunity`)** | **128 – 384** |

As propostas agora são ações que o motor executa de verdade.

## O resultado: 41 propostas, zero aceitas

Três buscas, fita 0 do `yhay_router_0908`, adversários `thomas_t95` e `aberatozer_d5e3`,
dois assentos, seeds `dev` disjuntas por experimento, oito propostas e duas rodadas cada.

| bloco | busca | check | propostas | pior oponente antes/depois | delta no check |
|---|---|---|---:|---|---:|
| 72:144 | `1038:1042` | `1042:1046` | 9 | 0,75 / 0,75 | 0,000 |
| 144:288 | `1030:1034` | `1034:1038` | 16 | 0,50 / 0,50 | 0,000 |
| 648:719 | `1046:1050` | `1050:1054` | 16 | 0,75 / 0,75 | 0,000 |

Toda proposta legal deu **delta de vitória exatamente zero**, e várias deram delta de
margem exatamente zero também — regar, cuidar, colher e coletar fertilizante nos slots
ociosos daqueles blocos não mudou uma única partida. `CARE` é o caso mais claro: o bônus
só é pago se o animal também for alimentado no dia, e ele não é, então cuidar banca nada.

## A exceção, que é o achado

No bloco 72:144, **uma única `FEED` no turno 94** — legal, com o trabalhador parado sobre
um animal não alimentado e carregando trigo — custou:

| | |
|---|---:|
| delta de vitória | **−0,250** (CI95 [−0,75, 0,00]) |
| delta de margem | **−4 483 moedas** |
| ações sem efeito | 212 → **1 380** |

Um trigo. A proposta `ALL` do mesmo bloco reproduz exatamente o mesmo número, porque a
`FEED` domina as outras seis.

A leitura é a fragilidade, não a economia do animal: a fita é um **plano acoplado**.
Consumir uma unidade de inventário que o sufixo fixo contava em ter dessincroniza o resto
da temporada — as ordens de venda e as sequências `PICKUP`/`DROP` seguintes deixam de casar
com o estoque real, e 1 168 ações passam a não fazer nada. É o mesmo mecanismo que fez o
`budget_guard` do chassis desabar sobre estas fitas, medido agora por outro caminho.

## O que isso decide para a #39

1. **Slot ocioso não é déficit.** Nos três blocos medidos, todo trabalho admissível é
   inútil (delta zero) ou negativo. O passo de "trabalho de unidade" está esgotado nesta
   fita, e ampliar o orçamento de propostas não muda a conclusão: o espaço inteiro de
   oportunidades compartilhadas foi enumerado em dois dos três blocos.
2. **Qualquer gerador que consuma inventário precisa consertar o sufixo.** Sem isso, o
   ganho local é engolido pela dessincronização. Isso é exatamente uma camada de chassis, e
   coloca `sell_lead`/`clamp_sells` como pré-requisito de um gerador econômico, não como
   alternativa a ele.
3. **A fronteira que importa continua sendo a de blocos.** O prior público registrado na
   issue — fork por volta dos turnos 72–144 conforme as shops, e depois 0,6–3,9% dos turnos
   variando — aponta para trocar *blocos inteiros* entre fitas de mesma procedência, que é
   o passo 1/4 da issue, e não para editar ações dentro de um bloco.

Nenhuma submissão, nenhuma seed de validação ou holdout consumida, `release_status`
sempre `not_validated`. Evidência completa, com planos, hashes de geradores e histórico
por proposta, em [opportunity-search.json](opportunity-search.json).

## Reprodução

```bash
python -m experiments.block_solver --mutation-space opportunity \
  --source opponents/public/yhay_router_0908/actions.json --tape-index 0 \
  --start 144 --days 6 --proposals 8 --rounds 2 \
  --opponents clock::opponents/public/thomas_t95/main.py,clock::opponents/public/aberatozer_d5e3/main.py \
  --seeds 1030:1034 --check-seeds 1034:1038 --workers 4 \
  --output experiments/searches/opportunity-144-01
```
