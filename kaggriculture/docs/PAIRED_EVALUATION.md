# Comparação pareada e gate local — issues #33, #34, #36 e #38

A decisão competitiva usa vitórias, derrotas e empates (0,5), com a coorte forte
como métrica primária. Margem e dinheiro permanecem diagnósticos. O gate é uma
recomendação local; não envia arquivos e não substitui preflight nem a política
de agentes ativos investigada na #37.

## Um comando para as duas pernas

A partir de `kaggriculture/`, com o ambiente virtual ativo:

```bash
python -m arena.paired \
  --baseline clock::opponents/public/yhay_router_0908/main.py \
  --candidate clock::versions/v004/main.py \
  --opponents clock::opponents/public/thomas_t95/main.py,clock::opponents/public/aberatozer_v23/main.py,clock::opponents/public/yhay_router_0908/main.py \
  --seeds 1000:1100 --split dev --workers 4 \
  --mirrors yhay_router_0908 \
  --output experiments/results/paired-v004-dev
```

São 100 blocos × 3 oponentes × 2 assentos × 2 candidatos = 1.200 partidas.
`--strong-only` restringe o painel usando os ratings capturados no início da
execução e recusa um painel vazio. O agregado secundário então descreve somente
o painel selecionado; não é uma avaliação dos adversários excluídos.

O resultado contém `plan.json`, as duas ligas completas em `baseline/` e
`candidate/`, `comparison.json`, `gate.json` e um resumo em `report.md`.
Ratings, famílias, data de classificação, corte, hashes, ambiente e tempos ficam
registrados. Alterações posteriores nos ratings não mudam um gate já produzido.
A classificação dos ratings usa o contrato da #32; uma estimativa continua sendo
uma estimativa, mesmo quando sua fotografia foi preservada.

Os dois candidatos são declarados no mesmo lote do registro antes da primeira
callback. A primeira perna consome a validação, a segunda é readmitida no lote.
Uma falha não devolve seeds. Um resultado parcial produz `failure.json`, sem gate
favorável. Diretórios existentes, arquivos ausentes, painel vazio e seeds
inválidas são recusados antes de qualquer consumo. O driver mantém um processo
novo por partida; não altera o isolamento para ganhar velocidade.

`--min-blocks 2` permite um smoke test pequeno. O gate de release continua exigindo
100 blocos e validação independente. O exemplo acima é desenvolvimento e recebe
`NO SUBMIT` independentemente do desempenho.

**Não há 100 seeds inéditas na reserva atual:** restam `100125:100200` (75).
Uma validação de 100 blocos exige registrar uma nova faixa, com proveniência e
auditoria de uso anterior. Esta implementação não amplia o registro nem consome
holdout. Seeds usadas na busca do solver da #39 pertencem a desenvolvimento.

## Comparar resultados existentes

```bash
python -m eval.ladder experiments/results/val-y_bare \
  experiments/results/val-y_lead_only \
  --as-of 2026-09-08 --mirrors yhay_router_0908 \
  --output experiments/results/v004-comparison.json
python scripts/submit_gate.py experiments/results/v004-comparison.json
```

`--ratings FILE` aceita uma tabela congelada ou o envelope de `ratings.json`.
Use a tabela original para reproduzir exatamente uma classificação histórica;
`--as-of` sozinho muda a data de corte, não recupera ratings antigos. A CLI lê o
split dos `summary.json` das duas ligas; metadados ausentes ou splits diferentes
não autorizam release. O gate confia em relatórios locais produzidos pelo
comparador: um JSON editado à mão não é uma prova autenticada.

## Garantias estatísticas

`eval.pairing` exige o mesmo painel, seeds e assentos, com blocos completos.
Recusa duplicatas, aliases de oponentes ambíguos, scores fora de 0/0,5/1, falhas,
mudança de candidato dentro de uma perna, mudança de adversário, backend,
configuração ou ambiente. A configuração pode variar apenas no campo `seed`,
que precisa concordar com a seed da partida. Os adapters fazem parte da identidade
comparada; `clock::x` e `x` não viram o mesmo oponente silenciosamente.

O delta é a diferença pareada de scores. O bootstrap percentil reamostra blocos
de seeds inteiros, mantendo assentos e oponentes juntos: 10.000 reamostragens,
PRNG seed 771, ordem canônica independente da ordem dos arquivos. Um único bloco
não produz intervalo de confiança para o delta.

A fixture `tests/fixtures/v004-paired.json` preserva os 350 pares históricos,
placares, margens diagnósticas, hashes dos agentes e hashes dos dois arquivos
originais. Não houve novas partidas nem uso de validação para esta reprodução:

| Recorte | Delta | CI95 reproduzido |
|---|---:|---:|
| Sete oponentes | +0,080000 | [+0,045714; +0,114286] |
| Sem yhay | +0,016667 | [−0,026667; +0,060000] |

Os valores manuais anteriores eram [+0,044; +0,116] e [−0,030; +0,063]. Os deltas
foram reproduzidos; os limites exatos não. Mantemos aqui o resultado determinístico
calculado dos dados preservados, em vez de ajustar o teste para reproduzir uma
anotação. Como verificação adicional, 100.000 reamostragens deram
[−0,026667; +0,063333] no recorte sem espelho. A conclusão não muda.

## Política executável

`SUBMIT` exige validação identificada, pelo menos 100 blocos, delta forte positivo
com limite inferior do CI95 acima de zero, nenhuma regressão pontual contra um
oponente forte e delta agregado não negativo. O efeito também precisa sobreviver
à remoção de cada oponente forte e de cada família forte. O agrupamento usa o
campo `family` do registro; famílias mal identificadas continuam sendo uma
limitação da evidência. Exigem-se pelo menos duas famílias fortes.

A tolerância de regressão é zero nesta versão da política. Isso é conservador:
perder significância ao retirar uma família indica evidência insuficiente para
promoção, não prova que todo o ganho veio dela. Não fazemos uma previsão de rating
Bradley–Terry a partir desse gate.

Espelhos byte a byte do baseline são detectados automaticamente. Compartilhamento
de fitas em arquivos diferentes é declarado com `--mirrors`, porque os registros
históricos de partidas não guardam essa relação. O gate v004 retorna `NO SUBMIT`
e identifica `yhay_router_0908` como espelho/compartilhamento de fitas cuja remoção
não deixa evidência positiva suficiente. Também aponta os apenas 25 blocos.

## Auditoria de seleção e compatibilidade

- `tape_screen`: pior placar por oponente, placar agregado, digest estável; margem
  não desempata. `--limit` usa ordem de digest, inclusive em bibliotecas antigas.
- `tape_harvest`: filtra pelo resultado da partida e ordena por score/digest;
  `--min-margin` foi removido. Use `--min-score`.
- `episode_tapes`: ordena por digest; o filtro opcional de vencedores compara
  resultados apenas para determinar quem venceu, sem ordenar pela magnitude.
- `tape_agent.select`: ignora a ordenação antiga por dinheiro/margem.
- O sweep de animais desempata por tipo/quantidade estáveis. O torneio de bases já
  selecionava por placar da pior família e dispersão de placares, sem margem.
- Resumos novos usam `mean_margin_diagnostic` e `median_margin_diagnostic`;
  rankings usam `margin_diagnostic`; CSV/HTML/Markdown identificam o diagnóstico.
  Os registros brutos mantêm `margin` para ler evidência histórica. Os deltas
  econômicos de `eval.compare` recebem `role: diagnostic`.

Relatórios e artefatos históricos não são reescritos. Seus critérios antigos não
são critérios de promoção atuais. A busca interna de um solver pode usar dinheiro
ou valor de estado como aproximação para gerar candidatos; a seleção competitiva
final deve passar pela avaliação por vitórias. Esta auditoria não altera o solver
em desenvolvimento na #39.
