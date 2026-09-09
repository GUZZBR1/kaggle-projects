# O painel como dataset versionado

Fecha a issue #45.

`eval/standing.py` já fazia a pergunta certa — taxa de vitória absoluta por faixa de rank,
assento e lineage, com CI e piso estrutural — e recebia a resposta de *quem está em qual
faixa* como um `--ranks` digitado ao lado da execução. É a mesma passagem manual que
`eval/dossier.py` existe para eliminar, um nível abaixo: um standing correto sobre uma
população que ninguém consegue reconstruir é um número sobre um conjunto sem nome.

Rank ao vivo também não serve como autoridade. Ele atrasa, depende da trajetória da
submissão e os agentes mais fortes são retirados do ladder, então o melhor oponente
observável não é o melhor existente. O que pode ser autoridade é uma **observação datada**,
presa a um artefato que temos byte a byte e guardada para sempre.

## O que é uma revisão

`eval/panel.py` junta três fontes e não aceita nenhuma delas sozinha:

| fonte | o que ela é a autoridade de |
|---|---|
| `opponents/manifest.json` + `opponents/public/*/main.manifest.json` | o artefato: `sha256`, família/lineage, motor, origem |
| `opponents/ratings.json` | o rating datado e o `kind` dele |
| `opponents/panel-observations.json` | o rank datado, o `kind` dele e o snapshot de leaderboard que o produziu |

O resultado é uma revisão em `opponents/panels/panel-<revision>.json`. A `revision` é o
sha256 do conteúdo mais a política; duas construções a partir das mesmas entradas dão a
mesma revisão, e qualquer mudança dá outra. `built_at` fica fora do hash: é quando o
arquivo foi escrito, não parte do que ele afirma.

## Um rank é evidência do quê

A assimetria de `docs/RATINGS_REFRESH.md` vale igual para rank. O rank observável é o do
**time do autor**, que limita o artefato publicado **por cima**:

- `direct` — nossa própria submissão do artefato idêntico: coloca em faixa;
- `author_current` — o time enquanto o artefato fixado é a publicação mais nova dele:
  coloca em faixa, com o viés registrado em `RATINGS_REFRESH.md`;
- `author_upper_bound` — o time para um artefato já substituído: **nunca** coloca em
  faixa. Um limite superior pode provar que um agente *não* é top 10 e jamais que ele é.

Bandar por um limite superior fabricaria exatamente a cobertura que o gate existe para
exigir, então ele não banda nada.

`eval/panel.py` também recusa o oponente cujo `kind` de rank discorda do `kind` de rating:
são dois arquivos descrevendo a mesma observação, e discordância significa que um foi
editado sem o outro.

## Admissão

Um oponente de painel tem que ser aquilo que ele diz que é, byte a byte. Um notebook
(`kernel`) ou um commit de repositório é essa afirmação e nós temos o arquivo. Uma
**reconstrução** não é: é a alegação de que algum episódio jogaria daquele jeito, e só vale
depois que o episódio nomeado for reproduzido. Gerar e verificar essas reproduções é a
**#39**; recusar as não verificadas é trabalho deste módulo, e a regra existe *antes* das
fitas justamente para que elas não entrem em silêncio.

```json
"reconstruction": {"episode": "12345",
                   "reproduction": {"episode": "12345", "digest": "…", "verified_at": "…"}}
```

Sem o bloco `reproduction` completo, o artefato é recusado do painel — e recusado
explicitamente, com o motivo no campo `refused` da revisão, nunca omitido.

## O gate recusa, nunca aprova por omissão

- **freshness**: painel observado há mais de `MAX_PANEL_AGE_DAYS` (7) dias. O campo público
  se reordena todo dia; ratings toleram 14 porque rating é uma estatística lenta sobre um
  time, enquanto pertencer a uma faixa é uma afirmação sobre um leaderboard diário. A idade
  do painel é a do membro **mais velho**, não a do mais novo: senão um oponente vencido
  entra na carona de um recém-observado.
- **faixa decisiva vazia** (`top10`, `rank10_30`): não há aritmética que conserte isso.
- **faixa carregada por uma lineage só**: mede a família, não a faixa. Mínimo de 2.
- **concentração**: uma lineage com mais de 50% da faixa — a segunda lineage deixou de
  conferir a primeira.

`eval/standing.py` dobra essas recusas dentro do próprio gate dele, prefixadas por
`Panel:`, e `eval/dossier.py` as repete como falha do candidato. Um standing sobre um
painel que não sustenta a pergunta não é um passe mais fraco: não é resposta.

## Imutabilidade

`save()` escreve o arquivo uma vez. Refilar a mesma revisão é no-op; filar conteúdo
diferente sob uma revisão já ocupada é erro. `opponents/panels/index.json` é append-only —
é o registro do que acreditávamos e quando, não uma visão do que acreditamos agora.
`load()` recusa um arquivo cujo conteúdo não bate mais com o nome sob o qual está filado.

Atualizar o meta cria revisão nova; não reescreve a evidência de uma decisão passada.

## Uso

```bash
# ver o painel que as fontes atuais produzem, sem escrever nada
.venv/bin/python -m eval.panel

# filar a revisão
.venv/bin/python -m eval.panel --write

# um standing que sabe contra o que ele ficou de pé
.venv/bin/python -m eval.standing experiments/results/<run> \
  --panel opponents/panels/panel-<revision>.json \
  --candidate v009 --output experiments/results/v009-standing.json
```

`--panel` e `--ranks` são mutuamente exclusivos: o snapshot já carrega os ranks e as
lineages, e passá-los ao lado é a divergência que ele elimina. A forma `--ranks` continua
existindo para diagnóstico, e o relatório dela diz `panel: null` — ela não consegue nomear
contra o que mediu, e `eval/dossier.py` age de acordo.

## O que o painel de 2026-09-08 diz

```
PANEL ce52cf88cacf  observed 2026-09-08
gate = FAIL

  top10         0 opponent(s)  0 lineage(s)  empty  decisive
  rank10_30     0 opponent(s)  0 lineage(s)  empty  decisive
  rank30_100    2 opponent(s)  2 lineage(s)  concentration 50%
               yamakawanin_king_v4e, yhay_router_0908
```

O melhor artefato público fixado é o `yhay_router_0908`, cujo time está em rank 45. As duas
faixas decisivas estão vazias, então **nenhum standing absoluto construído sobre este painel
autoriza um envio** — e é isso que `eval/dossier.py` já vinha reportando desde a #47. A
diferença é que agora a recusa vem do painel, com proveniência, em vez de ser uma
consequência lateral de um `--ranks` que ninguém guardou.

`tests/test_panel.py::test_the_real_panel_cannot_support_a_release_standing_yet` fixa esse
estado. Quando um oponente de top 10 for fixado, é esse teste que muda — deliberadamente.

## O que fica de fora

Gerar nossas próprias fitas é a **#39**; distribuir partidas é a **#43**; enviar ao Kaggle
não acontece em lugar nenhum deste módulo.
