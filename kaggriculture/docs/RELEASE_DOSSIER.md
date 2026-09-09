# Dossiê de release — issue #47

`eval/dossier.py` produz um veredito único sobre um envio, a partir dos relatórios que
já existiam separados. Ele é somente leitura: não envia nada ao Kaggle, não lê a conta
do Kaggle e não roda partidas.

## O problema que ele resolve

Quatro perguntas diferentes já tinham resposta, cada uma em seu relatório:

| pergunta | quem responde |
|---|---|
| o candidato ganha do agente que ocupa o nosso slot? | `arena.paired` + `eval.submit_gate` |
| ele é forte em termos absolutos contra o meta? | `eval.standing` |
| o arquivo exato que subiria joga uma temporada? | `submission.preflight` |
| o que este envio custa em histórico e quota? | `docs/FINAL_SUBMISSION_POLICY.md` |

O risco nunca esteve dentro de nenhuma delas. Está na passagem manual entre elas: uma
comparação sobre um artefato citada ao lado de um standing sobre outro, ou ao lado do
preflight de um arquivo que não foi o que se avaliou. Ler três relatórios corretos como
uma decisão é o único passo que nenhum relatório confere.

## Recusa antes de avaliar

O módulo repete a separação que `eval/submit_gate.py` já fazia:

- **recusa (binding)** — "estes relatórios não falam da mesma coisa". Vira `NO DECISION`.
- **falha (criteria)** — "falam, e a resposta é não". Vira `NO SUBMIT`.

As recusas são todas *entre* relatórios, nunca dentro de um:

1. `comparison.snapshot.candidate_hash`, `standing.provenance.candidate_hash` e
   `preflight.sha256` têm que ser o mesmo SHA-256.
2. O standing precisa ter proveniência. Carregado de `matches.csv` ele não tem: o CSV
   descarta as colunas de hash. `eval.standing` apontado para o diretório da execução lê
   `matches.jsonl`, que as preserva.
3. Fingerprint do motor igual nos três relatórios; backend igual entre comparação e
   standing.
4. Onde os dois painéis se sobrepõem, o mesmo adversário tem que ser o mesmo artefato.
   Os painéis são populações diferentes de propósito — coorte pareada contra o incumbente
   e painel do meta — então não precisam ter os mesmos membros.

### A identidade que não fecha hoje

Um agente rodado **por nome** tem `agent_hash` = digest das fontes em `agent/` mais
`arena/agents.py`. Um agente rodado **por caminho** tem `agent_hash` = sha256 do arquivo,
que é exatamente o que o preflight reporta. As duas identidades só coincidem quando a
avaliação rodou o artefato construído.

A evidência gravada no repositório mostra o problema: `docs/incumbent-t95-comparison.json`
avaliou `fd478f8c…` e `versions/v004/preflight.json` voou `13344303…`. Ambos estão
corretos e não são a mesma identidade. `tests/test_dossier.py` fixa esse caso.

**Consequência operacional:** para uma decisão de release, rode a perna do candidato com
`--candidate versions/vNNN/main.py`, o arquivo construído, e não com um nome de agente.

## Critérios

Passada a amarração, o `SUBMIT` exige tudo ao mesmo tempo:

- `eval.submit_gate` = `SUBMIT` sobre a comparação pareada, cujo baseline é o ocupante
  do slot declarado;
- `eval.standing` com gate `PASS` **e** standing defendido (`safe`);
- seeds do standing classificados como `validation` pelo `seed_registry.json` — a
  classificação é perguntada ao `arena/seeds.py`, não lida de um campo do relatório;
- cada faixa decisiva (`top10`, `rank10_30`) com pelo menos dois adversários;
- snapshot de ratings dentro do `max_rating_age_days` que a própria comparação declara;
- `preflight.status == PASSED`;
- estado de slots e quota consistente.

## Slots, quota e calendário

O estado da conta é **declarado**, não lido. O arquivo `--slots`:

```json
{
  "checked_at": "2026-09-08T19:00:00+00:00",
  "daily_submissions_used": 1,
  "slots": [
    {"slot": "A", "id": "thomas_t95", "hash": "…", "submitted_at": "2026-09-01T00:00:00+00:00", "episodes": 412},
    {"slot": "B", "id": "v003", "hash": "…", "submitted_at": "2026-09-05T00:00:00+00:00", "episodes": 96}
  ]
}
```

O incumbente **não é redigitado**: nomear o slot basta, e o dossiê deriva dele o `id` e o
`hash` que `eval.submit_gate` confere contra a perna baseline que realmente rodou. Isso
elimina o último lugar onde os dois podiam divergir.

Recusas desta camada, todas de `docs/FINAL_SUBMISSION_POLICY.md`:

- declaração sem data ou com mais de 24 h — os slots giram por recência;
- dois finalistas deslocando o mesmo slot;
- finalista byte-idêntico a um agente já ativo (reenvio reinicia o histórico e não muda
  nada que é jogado);
- quota: `usados + planejados` acima de `5 − 2` reservados para recuperação;
- qualquer coisa depois de 29/09/2026 23:59 UTC, o corte de planejamento.

## Complementaridade

O time recebe a melhor das duas submissões, então o segundo slot vale o que ele cobre
que o primeiro não cobre. O dossiê compara os `per_lineage` dos dois standings e reporta
linhagens em que **ambos** ficam sob o piso, linhagens cobertas por exatamente um, e a
correlação entre eles.

É relatório, nunca veto: um par pode ser correlacionado e ainda assim ser as duas
melhores coisas que temos. Quem decide é quem lê.

## Uso

```bash
.venv/bin/python -m eval.dossier \
  --slots docs/active-slots.json \
  --candidate v009:A \
  --comparison experiments/results/v009-vs-incumbent.json \
  --standing experiments/results/v009-standing.json \
  --preflight versions/v009/preflight.json \
  --candidate v010:B \
  --comparison experiments/results/v010-vs-incumbent.json \
  --standing experiments/results/v010-standing.json \
  --preflight versions/v010/preflight.json \
  --output docs/release-dossier.json
```

`--candidate ID:SLOT` nomeia o finalista e o slot que ele deslocaria. Cada `--candidate`
consome um `--comparison`, um `--standing` e um `--preflight`, na ordem. `--ceiling` é
opcional e viaja ao lado da decisão como diagnóstico, sem nunca alterá-la.

A saída JSON registra, por finalista, os dois hashes, o `run_spec.sha256`, os dois gates,
o split dos seeds, o preflight, o slot deslocado e a lista completa de recusas e falhas;
e, uma vez por execução, o estado de slots, a complementaridade, as constantes da política
e o `audit` com o sha256 de cada arquivo lido.

## `run_spec`

`run_spec()` reúne os campos que não podem mudar em silêncio entre planejamento, execução
e decisão — motor, backend, configuração, corte de rating, hashes de ratings e famílias,
split, os dois painéis e os seeds do standing — e devolve um sha256 sobre eles. Dois
relatórios só descrevem a mesma execução se esse número for igual.

É um substituto compatível para a issue #46: os campos já existem hoje, espalhados por
dois relatórios. Quando o `RunSpec` versionado da #46 existir, ele passa a ser a
autoridade e esta função vira um adaptador.

## Limites conhecidos

- O dossiê não sabe nada da conta Kaggle. Tudo em `--slots` é palavra do operador; o que
  ele confere é consistência interna e idade da declaração.
- A independência de linhagens por faixa é da issue #45. Aqui só se exige dois
  adversários por faixa decisiva, que é o que o relatório de standing consegue sustentar.
- O painel atual não cobre `top10` nem `rank10_30`, então nenhum standing real passa hoje.
  Isso é a #45, e a recusa por faixa vazia é o comportamento correto enquanto durar.
