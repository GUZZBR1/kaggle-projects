# Ray privado para a #43

Ray apenas transporta lotes. Dentro de cada task, `arena.parallel.matches` ainda cria um
filho descartável por partida e o pai desse filho impõe o deadline. O head é o único
processo que admite seeds e escreve SQLite. O runtime exclui `seed_registry.json`, marca a
task e seus filhos como `ray-worker` e recusa no código tanto `admit_run` quanto abrir um
`JobStore` nesse papel. Jobs remotos com `replay` também são recusados: o resultado completo
volta no `BatchResult` e somente o head decide qualquer persistência final.

## Preparação dos dois PCs

Os dois nós precisam de Python 3.12, do mesmo checkout e do mesmo ambiente:

```bash
bash scripts/setup.sh --distributed
.venv/bin/python scripts/check_environment.py
```

Ray não fornece uma fronteira de segurança entre clientes e cluster. Use uma LAN privada
ou VPN e bloqueie as portas na interface pública. No head, reserve um ou dois CPUs ao
declarar os recursos e mantenha o dashboard preso a localhost:

```bash
.venv/bin/ray start --head --node-ip-address=HEAD_PRIVATE_IP --port=6379 \
  --dashboard-host=127.0.0.1 --num-cpus=CPUS_DISPONIVEIS
```

No segundo PC:

```bash
.venv/bin/ray start --address=HEAD_PRIVATE_IP:6379 \
  --node-ip-address=WORKER_PRIVATE_IP --num-cpus=CPUS_DISPONIVEIS
```

`CPUS_DISPONIVEIS` deve ser `CPUs lógicos - 1` ou `- 2`. O cluster não deve anunciar os
cores reservados: `--leave-cpus-free` no driver local não consegue corrigir recursos que
um worker remoto anunciou incorretamente.

## Gates antes de throughput

Do head, a prova obrigatória executa as mesmas 400 partidas em todos os nós, compara o
resultado relevante serializado exatamente e roda em cada nó um agente que desliga
`setitimer` e trava:

```bash
.venv/bin/python scripts/verify_ray_cluster.py --address=auto \
  --pairs=200 --output=docs/ray-cluster-verification.json
```

O comando recusa cluster de um único hostname, hash de agente diferente, fingerprint do
motor diferente, qualquer diferença exata no resultado e deadline remoto que não mate o
filho. Ao final, ele mata um worker Ray de verdade na primeira tentativa e exige que o
mapper reenvie aquele lote uma única vez. A morte e a recuperação são fixadas por afinidade
e repetidas em cada NodeID vivo; retries implícitos do Ray continuam desligados.

Somente depois rode o benchmark. Os quatro tamanhos têm papéis diferentes: 32 é smoke,
256 mede o scheduler local, 1024 mede throughput e 8000 representa a busca real.

```bash
.venv/bin/python scripts/benchmark_ray.py --address=auto \
  --jobs=32,256,1024,8000 --output=docs/ray-benchmark.json
```

Antes da medição distribuída, o script roda o lote inteiro pela pool local em **cada** nó,
usando todos os CPUs que esse nó anunciou ao Ray. O menor wall-clock vira a linha de base;
assim não existe a suposição de que o head seja o PC mais rápido. O relatório grava essas
linhas por hostname, jobs/s, speedup, eficiência paralela, p50 e p95 de partida, cauda de
lote e utilização de CPU. No workload representativo de 8 000 jobs, o comando falha se o
cluster não atingir ao menos 1,10× sobre o melhor `forkserver` local; esse limite pode ser
elevado com `--minimum-representative-speedup`. Uma série que inclui 8 000 também recusa
menos de dois hostnames distintos e mudança de membros durante a medição.

Referências operacionais: [segurança do Ray](https://docs.ray.io/en/latest/ray-security/index.html),
[tolerância a falhas de tasks](https://docs.ray.io/en/latest/ray-core/fault_tolerance/tasks.html)
e [runtime environments](https://docs.ray.io/en/latest/ray-core/handling-dependencies.html).
