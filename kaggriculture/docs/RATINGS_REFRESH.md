# O rating de cada oponente fixado, e como reatualizá-lo

Fecha a issue #32. A métrica primária (`eval/ladder.py`) é a taxa de vitória contra a
**coorte forte**, e coorte forte é uma afirmação sobre rating. Até aqui a coorte vinha de
duas observações soltas; agora todo oponente fixado tem um número datado ou um "não sei"
explícito, e `opponents/ratings.json` é a autoridade.

## O que é observável, e o que não é

O rating que interessa é o que **aquele artefato** teria no ladder. Isso só é diretamente
observável quando nós mesmos submetemos o arquivo byte a byte. Para todo o resto, o que
existe é o rating do **time do autor**, que limita o artefato **por cima**: o agente ativo
de um time pode ser melhor do que qualquer coisa que ele publicou, e não temos como detectar
o contrário.

O viés é medido, não suposto. O `thomas_t95` é o notebook mais recente do autor e o time
dele está em 2519,6; a nossa própria submissão do mesmo arquivo rateou **2359,8**. O proxy
superestimou o artefato em cerca de 160 pontos.

Daí os três `kind`, que não autorizam a mesma conclusão:

| `kind` | o que é | como a coorte usa |
|---|---|---|
| `direct` | nossa submissão do artefato idêntico | decide, nos dois sentidos |
| `author_current` | rating do time do autor **enquanto** o artefato fixado é o notebook mais novo dele | decide, com o viés acima registrado |
| `author_upper_bound` | rating do time do autor para um artefato que ele já substituiu | **abaixo** do corte prova `weak`; **no ou acima** do corte não prova nada e vira `unknown` |

Ausente, velho (mais de 14 dias) e `unknown` caem **fora** da coorte forte, nunca dentro.
Deixar um oponente não medido entrar por omissão decidiria em silêncio exatamente o que a
métrica primária existe para medir.

O `author_current` continua sendo um limite superior — o certo seria só `direct`. Ele é
admitido porque é a observação atribuível mais próxima e porque sem ele a coorte forte fica
com um oponente só, e uma métrica primária de um espelho só é pior que um proxy com viés
documentado. Quando uma submissão nossa medir um desses artefatos diretamente, o `kind`
sobe para `direct` e o viés some.

## Estado em 2026-09-08

| oponente | rating | `kind` | coorte |
|---|---:|---|---|
| `yhay_router_0908` | 2712,5 | `author_current` | **forte** |
| `aberatozer_v23` | 2618,5 | `author_current` | **forte** |
| `thomas_t95` | 2359,8 | `direct` | **forte** |
| `thomas_t93` | 2519,6 | `author_upper_bound` | `unknown` (limite acima do corte) |
| `kaitofukami_v48` | 2491,9 | `author_upper_bound` | `unknown` (limite acima do corte) |
| `boatlee_v21` | 1997,2 | `author_upper_bound` | fraco |
| `boatlee_v16` | 1997,2 | `author_upper_bound` | fraco |
| `seyamalam_v21` | 940,0 | `author_upper_bound` | fraco |
| `cok_v10` | — | — | `unknown` (sem conta atribuível) |
| `lonespear_v11` | — | — | `unknown` (sem conta atribuível) |

O corte é 2 300 (`STRONG_CUT`), parametrizável por `--cut`.

## O procedimento

```bash
python scripts/refresh_ratings.py
```

Ele baixa o leaderboard público do dia, indexa por username, e para cada bundle fixado que
veio de um notebook: acha o time do autor, pergunta ao `kaggle kernels list` qual é o
notebook mais recente daquele autor nesta competição, e propõe `author_current` ou
`author_upper_bound` conforme o artefato fixado ainda seja ou não o mais novo. Ele
**não escreve** `ratings.json`: promover um limite a `author_current` é uma afirmação sobre
supersessão, e ela passa por leitura humana.

Comandos individuais, se for preciso conferir à mão:

```bash
kaggle competitions leaderboard kaggriculture -d -p .   # CSV com Rank, Score, usernames
kaggle kernels list --user <autor> --competition kaggriculture --sort-by dateRun
kaggle competitions submissions kaggriculture           # os nossos, para os `direct`
```

Depois de editar `opponents/ratings.json`, propague para o manifesto de cada bundle e para
`opponents/manifest.json`. O `tests/test_ratings.py` recusa qualquer divergência entre as
três cópias, então uma propagação esquecida quebra a suíte em vez de decidir a coorte em
silêncio.

## Com que frequência

O limite de idade é de 14 dias, mas ele é o ponto em que o número deixa de contar, não o
alvo. O campo público muda todo dia. Reatualize junto com a varredura de painel da issue
#35 — as duas leem o mesmo CSV — e sempre antes de usar a métrica primária para decidir uma
submissão.

## Quando um oponente cruza a fronteira

Um oponente que sai da coorte forte **não é retirado do painel**: o ajuste final roda sobre
quem continuar ativo, não sobre um corte formal de rating, e um candidato que desaba contra
uma família fraca continua sendo um candidato com um buraco. Ele apenas deixa de contar na
métrica primária e continua na secundária. O caminho contrário — um oponente que sobe acima
do corte — muda o denominador da métrica primária, então qualquer comparação pareada
anterior àquele momento não é comparável com uma posterior: refaça o `baseline` antes de
comparar.
