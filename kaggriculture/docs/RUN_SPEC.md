# RunSpec e manifesto de evidência

Fecha a issue #46.

## O problema

As garantias locais do projeto são boas e estão espalhadas. `arena.league`, `arena.paired`,
os experimentos, `eval.standing`, `eval.submit_gate` e os scripts de benchmark carregam cada
um os próprios defaults de workers, seeds, painéis, thresholds e output. `config.yaml`
resume parte deles enquanto `seed_registry.json`, os manifests de oponente e constantes
Python são as autoridades reais.

A consequência não é hipotética: **hoje é possível rodar a estratégia certa sob uma
combinação de parâmetros que não é o experimento que o relatório parece nomear**, e nada
depois disso percebe.

## O que entra no `run_id`, e o que não entra

A linha é *o que o run mediu*, não *como ele foi executado*.

| material (entra no `run_id`) | por quê |
|---|---|
| agentes (spec + sha256), oponentes (sha256 + lineage) | trocar um artefato é medir outra coisa |
| painel (`revision` + `observed_at`) | a população contra a qual o número significa algo (#45) |
| seeds, split, `registry_revision`, `registry_sha256` | evidência inédita e evidência já vista não são a mesma evidência |
| backend e fingerprint do motor | motor diferente, jogo diferente |
| `deadline_seconds`, `attempts` | um deadline muda resultados; política de retry muda o que é uma falha |
| `min_blocks`, `cut`, `max_rating_age_days`, `lineage_floor`, `safe_top20`, bandas, **gate** | quem vai ler o resultado, e sob que régua |

| incidental (fica de fora) | por quê |
|---|---|
| `distribution`: topologia, workers, cpus por task, batch size, endereço Ray | a **#43** mediu lotes bit-exatos entre nós. Um run começado local e retomado no cluster **é o mesmo run** e tem que poder dizer isso |

O `gate` é campo material de propósito: um run cujo leitor não está declarado pode ser lido
por qualquer gate que ele passe.

## Validação antes de consumir

`arena/seeds.py` queima seeds de validação reservadas **antes** da primeira callback. Um run
recusado depois disso já gastou a evidência que precisava para descobrir que estava mal
configurado. Por isso `runspec.validate()` faz tudo que é conferível sem mutar nada — hashes
presentes, ids de oponente não ambíguos, seeds únicas e classificadas pelo registro,
revisão e sha do registro batendo com o que o registro diz, backend válido, fingerprint
presente, `min_blocks` compatível com a quantidade de seeds, deadline e attempts sãos — e só
um spec que passou chega ao `admit_run`.

Painel é opcional aqui: a população de uma comparação pareada é a lista `opponents`, que já
está no spec. Painel é exigido para **ler** um run como standing absoluto, e isso é a #45,
aplicada em `eval/standing.py` e `eval/dossier.py`. O que este módulo recusa é uma
referência de painel pela metade, que pareceria uma população nomeada sem nomear nada.

## Resume só reaproveita jobs do próprio run

`job_id` cobre candidato, oponente, seed, assento, backend, split e os dois hashes — tudo
que decide se dois jogos são o mesmo jogo. Ele **não** cobre deadline, painel ou thresholds.
Dois specs que diferem só nisso produziam job ids idênticos, então um `--resume` serviria
jogos do outro experimento sem que nada notasse.

`arena/jobs.py` passa a ter uma tabela `run` com um único `run_id`. Um store **adota** o
primeiro run que o reivindica — é o que mantém resumível um store escrito antes dos specs —
e depois disso nunca troca de mãos:

```
ValueError: …/baseline.jobs.sqlite3 holds games for run 3f2a…, and this run is 9b41….
Resume reuses only the games of its own run; the two specs differ in something job
identity cannot see.
```

## O manifesto

Um `run_id` que nada aponta não prova nada. `runspec.manifest(spec, evidence)` amarra o
spec ao store SQLite, à comparação pareada, ao standing, ao preflight e ao artefato final
pelos hashes de bytes, e lê o run declarado por cada peça — no JSON, para relatórios; na
tabela `run`, para stores.

Três vereditos, e nenhum deles é "provavelmente":

- `BOUND` — toda peça declara este run;
- `REFUSED` — alguma peça declara **outro** run, nomeado na recusa;
- `PARTIALLY BOUND` — alguma peça não declara run nenhum. Relatórios escritos antes dos
  specs são exatamente isso: continuam legíveis, e nenhum manifesto finge que estavam
  amarrados.

## Migração

- `arena.paired` escreve `spec.json` e `manifest.json` ao lado do `plan.json` de sempre, e
  carimba `run_id` na comparação e no gate. `plan.json` continua existindo e ganhou o campo.
- `eval.dossier.run_spec()` virou **adaptador**, como a #47 prometeu: quando a comparação
  declara um `run_id`, ele é a resposta; quando não declara, a reconstrução campo a campo
  continua servindo o relatório antigo. O `binding()` do dossiê recusa relatórios que
  nomeiam runs diferentes.
- Todo relatório declara `schema_version`; nada histórico deixou de ser legível.

## Uso

```bash
# rodar, com o spec escrito e o manifesto amarrado
.venv/bin/python -m arena.paired --baseline champion --candidate versions/v009/main.py \
  --opponents yhay_router_0908,yamakawanin_king_v4e --split validation \
  --panel opponents/panels/panel-<revision>.json \
  --deadline-seconds 30 --output experiments/results/v009

# reler o spec e amarrar evidência que veio depois
.venv/bin/python -m arena.runspec experiments/results/v009/spec.json \
  --evidence standing=experiments/results/v009-standing.json \
  --evidence preflight=versions/v009/preflight.json \
  --output experiments/results/v009/manifest.json
```

`arena.runspec <spec>` sozinho revalida o spec contra o registro atual e imprime o run.
`load()` recusa um spec editado depois de escrito: um `run_id` que não segue o próprio spec
é pior que nenhum, porque tudo depois dele confia.

## O que fica de fora

Gerar fitas próprias é a **#39**; o transporte Ray é a **#43**. Este módulo não envia nada
ao Kaggle e não lê a conta.
