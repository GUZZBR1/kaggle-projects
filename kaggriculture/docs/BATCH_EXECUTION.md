# A camada de lote: o que a #43 precisa antes do Ray, medido num PC só

Entrega parcial da #43. **Não instala Ray e não distribui nada ainda** — constrói a costura
que um transporte remoto vai usar, e verifica num PC só as duas coisas que a issue diz que
precisam estar verificadas antes de confiar em qualquer número distribuído.

## Por que lote, e não uma partida por task

Ray reaproveita processos worker entre tasks. Uma partida por task desfaria em silêncio a
garantia que o `arena/parallel.py` existe para dar: um bundle de terceiro roda código em
tempo de import, o `arena/agents.py` consegue *notar* um rebind mas não desfazê-lo, e o
desfazer é a fronteira de processo. `@ray.remote(max_calls=1)` devolveria o isolamento
matando o worker a cada task, mas o startup de worker do Ray é mais pesado que o `spawn`
que acabamos de eliminar — ficaria mais lento do que não distribuir.

Então **o lote é a unidade de distribuição e a partida continua sendo a unidade de
isolamento**. `arena/batch.py` é essa camada, e ela roda hoje sem Ray.

## A costura

```
arena.jobs.execute(jobs, store, split, runner, workers=...)
                                     ^
                       arena.batch.batched_runner(size=32, map_batches=...)
                                                            ^
                                       o único ponto que um transporte Ray substitui
```

`map_batches(batches, workers)` devolve um envelope por lote, na ordem dos lotes; o padrão
executa aqui mesmo. As linhas saem **na ordem dos jobs** de qualquer forma, porque o
`execute` e todo chamador que casa job com linha o fazem por posição. Um transporte que
perca um lote é recusado em vez de parecer execução completa.

`worker_budget(cpus_free=1)` é a política de CPU: deixa um ou dois cores para a máquina,
e nunca devolve menos de um worker. Uma execução que deixa o host inutilizável é
interrompida por um humano, e execução interrompida é pior que execução lenta.

## O risco que a issue mandou checar

> `arena/match.deadline()` usa `signal.setitimer`, que só funciona na thread principal de um
> processo POSIX. Se a task rodar fora dela, o código cai silenciosamente no caminho de
> fallback.

Verificado, com teste: **não importa**. Cada partida roda na thread principal do seu próprio
filho, então o timer é armado onde ele funciona, independentemente de quem chamou o lote. E
a barreira real da #44 vive no **pai** de cada partida, não no timer — um bundle que trava é
morto pelo `killpg` mesmo com o timer desarmado. O teste dirige um lote a partir de uma
thread secundária e exige que o travamento morra assim mesmo.

O outro invariante testado é o que autoriza distribuir: **cortar o trabalho em lotes não
muda uma linha sequer**. Tamanhos 1, 3 e 10 produzem placar, dinheiro e dinheiro do rival
idênticos ao da pool direta.

## Medição nesta máquina

16 cores, `forkserver`, 32 partidas `v004` × `thomas_t95`, backend `fast`. O benchmark
recusa publicar throughput se as linhas divergirem entre configurações.

| workers | direta | em lotes de 8 |
|---:|---:|---:|
| 1 | 0,675 s/partida — 1,48/s | 0,594 s/partida — 1,68/s |
| 2 | 0,313 s/partida — 3,20/s | 0,308 s/partida — 3,24/s |
| 4 | 0,166 s/partida — 6,02/s | 0,166 s/partida — 6,04/s |
| 8 | 0,097 s/partida — 10,26/s | 0,100 s/partida — 10,03/s |
| 14 | **0,083 s/partida — 12,06/s** | 0,097 s/partida — 10,27/s |

Até 8 workers o lote não custa nada. Em 14 ele custa 15%, e a razão é aritmética, não
overhead: 32 partidas em lotes de 8 são **quatro** lotes para catorze workers, então a
cauda do último lote domina. A regra que sai daí é a mesma que a issue já propunha por
outro motivo — lotes pequenos, e muitos deles em relação ao número de workers. Com 8 000
partidas de busca, lotes de 32 dão 250 lotes, e a cauda desaparece.

Speedup de 7,2× de 1 para 14 workers. Reprodução:

```bash
python scripts/benchmark_pool.py --games 32 --workers 1,2,4,8,14 \
  --output docs/pool-benchmark.json
```

## O que **não** está entregue

- **O transporte Ray.** É uma função: `map_batches` rodando `@ray.remote(num_cpus=N)`.
  Não faz sentido escrevê-la sem uma segunda máquina para exercitá-la.
- **Determinismo entre nós.** O `money` do motor é float, e igualdade exata entre CPUs
  diferentes é provável mas não óbvia. É a única coisa que autoriza somar resultados de
  máquinas distintas num agregado, e não pode ser testada aqui.
- **Rede.** LAN privada ou VPN, sem dashboard exposto, sem token no git.
- **`--cpus-per-worker`.** Só significa alguma coisa com o escalonador do Ray.

A #43 continua aberta por esses quatro itens. O que ela já tem é a camada que eles vão usar,
com o isolamento e o deadline preservados um nível abaixo, e uma linha de base local honesta
para comparar contra qualquer ganho distribuído que se alegue depois.
