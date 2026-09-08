# O guarda de deadline estava do lado errado da fronteira

Fecha a issue #44. O limite por turno do harness era `signal.setitimer`, armado **dentro do
interpretador que executa o bundle adversário**. Duas linhas no bundle desligam:

```python
signal.signal(signal.SIGALRM, signal.SIG_IGN)
signal.setitimer(signal.ITIMER_REAL, 0)
```

Com `actTimeout = 1s`, uma sonda que gastou 3 segundos a mais num turno terminou a partida
com `failures: []`. O estouro não foi detectado de forma alguma. E um bundle que simplesmente
não retorna travava o worker para sempre, sem nada para notar.

## As três peças

**1. Deadline duro no pai, com kill do grupo.** `arena/parallel.py` deixou de usar
`ProcessPoolExecutor` e passa a supervisionar um processo por partida diretamente. O filho
chama `os.setsid()` antes de jogar, então um `killpg` alcança também os subprocessos que o
bundle tenha criado. O limite é `MATCH_TIMEOUT`, 300 s por padrão — duas ordens de grandeza
acima de qualquer partida medida aqui, porque ele existe para acabar com um travamento, não
para policiar agente lento. `ARENA_MATCH_TIMEOUT` ajusta; `timeout=None` desliga para quem
tem supervisão própria. Em Windows não há grupo de processos, e o kill alcança só o filho.

As linhas continuam saindo **na ordem dos jobs**, independentemente da ordem em que
terminam, porque os chamadores casam job e resultado por posição.

**2. Verificação de tempo decorrido depois da callback.** `arena/match.py` mede o turno com
`perf_counter` e, se o retorno veio depois do `actTimeout`, registra falha
`TimeoutError`. Isso não pré-empta nada — mas lê um relógio em vez de um handler, então
desarmar o timer deixa de esconder o estouro. É o que transforma a sonda da issue de
`failures: []` em falha registrada no passo 0.

**3. `signal` no `WATCHED`.** Um bundle que religa `signal.setitimer` ou `signal.signal`
aparece no relatório de adulteração. Isso é diagnóstico, não proteção, e a distinção
importa: estado de handler não é atributo de módulo, então um bundle que só chama
`signal.signal(SIGALRM, SIG_IGN)` passa por essa checagem intocado. Esse caso é pego pela
peça 2 e, no limite, pela peça 1.

## O que uma partida morta vale

Uma partida morta vira uma linha com o mesmo formato de qualquer outra, com `timed_out` e
falha `MatchTimeout` **nos dois lados**. Não dá para atribuir um travamento a um dos agentes
de fora do processo, e adivinhar creditaria uma vitória que não jogamos ou concederia uma
que não perdemos. Os dois lados falhando pontuam 0,5 pela mesma regra que o `run_match` já
usa, e toda comparação em `eval/` recusa evidência com falha de callback — então a partida
morta **invalida a comparação** em vez de virar empate silencioso.

E ela **nunca é repetida automaticamente**. Repetir faria o harness selecionar agentes que
"dão certo se você tentar algumas vezes", que é exatamente o que o preflight existe para
recusar. A distinção que a #42 vai precisar já está aqui: morte de worker sem resultado
levanta erro de infraestrutura; estouro de deadline é resultado de falha.

## Os testes que sustentam isso

`tests/test_deadline_barrier.py`:

- a sonda da issue — desarma o timer e estoura o turno — passa a registrar falha;
- um agente honesto não é acusado de estourar;
- um bundle que desarma o timer e **trava para sempre** é morto dentro do limite, a linha
  sai como `MatchTimeout`, e o outro job do mesmo lote joga normalmente: uma partida
  envenenada não envenena o lote;
- o subprocesso que o bundle iniciou morre junto (POSIX);
- o timeout não pode ser configurado como zero ou negativo, e pode ser desligado;
- `signal` está no `WATCHED` e um bundle que religa `setitimer` é reportado.

Um efeito colateral do teste novo expôs uma fragilidade em `tests/test_isolation.py`: o
sentinela lia o caminho do log de uma variável de ambiente, e um worker forkado herda o
ambiente de quando o **forkserver** subiu, não o de agora. Qual teste aquece o pool primeiro
era acidente alfabético. O caminho agora é embutido na fonte do sentinela.

## Escopo

Isto é defesa do nosso próprio harness contra os bundles públicos que nós mesmos
executamos, e é gate de liberação da #43: não se distribui execução de código adversário
sem esta barreira.
