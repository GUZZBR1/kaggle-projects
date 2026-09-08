# Varrer o campo público, e continuar varrendo

Fecha a issue #35. O painel estava congelado em 2026-09-07/08 e o campo público muda todo
dia — o próprio `yhay_router_0908` era um notebook atualizado horas antes de a gente
fixá-lo. Um painel de dois dias mede um campo que não existe mais.

## O critério

Entra no painel o artefato que satisfaz as três coisas:

1. **Está no campo forte.** O time do autor está em 2 300 ou mais no leaderboard público.
   O rating do time limita o artefato por cima; o que isso autoriza concluir está em
   `docs/RATINGS_REFRESH.md`.
2. **É proveniência completa.** O agente sai do notebook *verbatim*: uma célula
   `%%writefile main.py`, ou um literal base64 (eventualmente comprimido) que o próprio
   notebook decodifica. Nada de reconstruir por aproximação.
3. **Joga.** Uma temporada inteira contra o `starter` pelo carregador oficial, 719 passos,
   zero falhas de callback.

Nada é aposentado. Um oponente que cai da coorte forte continua na métrica secundária: o
ajuste final roda sobre quem continuar ativo, e um candidato que desaba contra uma família
fraca continua sendo um candidato com um buraco.

## O procedimento

```bash
# 1. quem está acima do corte, e quem publica
kaggle competitions leaderboard kaggriculture -d -p .
for p in 1 2 3 4 5; do
  kaggle kernels list --competition kaggriculture --page-size 100 --page $p \
    --sort-by dateRun --csv
done > kernels.csv
# juntar por username: autor do notebook -> time no CSV do leaderboard

# 2. fixar cada candidato, verbatim, com smoke game
python scripts/pin_notebook_agent.py <user>/<kernel> --id <pin_id> --dry-run
python scripts/pin_notebook_agent.py <user>/<kernel> --id <pin_id>

# 3. rating datado, e as três cópias em acordo
python scripts/refresh_ratings.py
```

O passo 2 escreve `opponents/public/<pin_id>/main.py`. Falta escrever à mão o
`main.manifest.json` (id, family, kernel, sha256, licença, engine, lineage e
`ladder_rating`), acrescentar a linha em `docs/public-opponent-registry.md` e a entrada em
`opponents/ratings.json`. O `tests/test_ratings.py` recusa qualquer bundle que não esteja
classificado, então esquecer uma dessas etapas quebra a suíte.

## O que a varredura de 2026-09-08 encontrou

450 notebooks da competição, cruzados com o leaderboard de 8 177 times. 28 autores acima de
2 300 publicaram algo; a maioria publicou análise, não agente. Fixados quatro:

| pin | rating do time | por que entrou |
|---|---:|---|
| `yamakawanin_king_v4e` | 2648,4 | fonte gzip+base64 com SHA-256 conferido pelo próprio notebook |
| `aberatozer_d5e3` | 2618,5 | sucessor do `aberatozer_v23`, que passa a ser limite superior |
| `lynnsakurai_v4` | 2572,7 | literal base64, Python puro |
| `reyhanksatria_v1` | 2427,3 | `%%writefile`, roda sozinho apesar do pacote nativo do notebook |

Recusados, com o motivo:

| candidato | rating | motivo |
|---|---:|---|
| `destbreso/v7-38-finance7-a-full-agent-layer-by-layer` | 2630,0 | o agente precisa de `agent.so` compilado a partir de fontes C++ **não publicadas** (kernel privado `v733-build-private`). Não é proveniência completa para nós. Vale registrar o que ele diz de si: é o roteador do `yhay81` verbatim mais duas camadas próprias, o que confirma a leitura de `docs/YHAY_ROUTER_FINDING.md` de fora |
| `flexonafft/kaggriculture-smart-farm-strategy-lab` | 2501,9 | é o `thomas_t93` com a docstring trocada; o blob de fitas é byte-idêntico. Re-skin, não família |
| `salemali7/kaggriculture-2900` | 1344,3 | o título anuncia 2 900+; o time do autor está em 1 344. O critério é o leaderboard, não o título |
| `bovard/kaggriculture-getting-started` | — | notebook oficial de exemplo, já coberto pelo `starter` |

## O que o painel novo diz do titular

O painel só vale se alguém jogar contra ele. `v004` contra as quatro famílias novas, 20
seeds `dev` (`1070:1090`), dois assentos, 160 partidas, zero falhas:

| oponente | coorte | win rate | W/T/L | margem (diagnóstico) |
|---|---|---:|---|---:|
| `aberatozer_d5e3` | forte | 0,750 | 30/0/10 | +3 848 |
| `yamakawanin_king_v4e` | forte | 0,850 | 34/0/6 | +10 224 |
| `lynnsakurai_v4` | forte | 0,950 | 38/0/2 | +7 884 |
| `reyhanksatria_v1` | forte | 0,950 | 38/0/2 | +10 503 |
| **`win_rate_strong`** | | **0,875** | | CI95 [0,775, 0,963] |

O `aberatozer_d5e3` é a família nova mais dura, e é o sucessor do chassis reativo que o
`CHASSIS_FINDING` já tinha apontado como o teto anterior. Nenhum empate em 160 partidas:
contra estas famílias não há espelho, o que confirma que elas não compartilham fitas com o
`v004`.

## Com que frequência

Junto com o refresh de ratings, e sempre antes de gastar uma submissão. As duas leem o
mesmo CSV do leaderboard, então rode as duas no mesmo dia — um painel novo com ratings
velhos classifica errado a coorte forte, que é o denominador da métrica primária.
