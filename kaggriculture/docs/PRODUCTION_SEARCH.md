# Busca de produção e trabalho — 08/09/2026

A etapa 2 da #39 está implementada: o solver agora gera tarefas de produção em
slots ociosos e troca a ordem de tarefas estacionárias da mesma unidade. A busca
mantém prefixo/sufixo, comandos de movimento e mercado, verifica a mesma fronteira
nos dois assentos e congela a escolha antes do check separado.

**Resultado: nenhuma das 16 variantes melhorou o placar.** A fita original foi
mantida nos dois experimentos. Isso não é uma submissão nova nem evidência de que
produção e trabalho não possam melhorar; são duas buscas pequenas, sobre uma fita
fixa e uma classe estreita de alterações.

| Bloco (turnos, intervalo semiaberto) | Busca dev | Check dev | Variantes | Partidas | Pior oponente antes/depois | Agregado antes/depois |
|---|---|---|---:|---:|---:|---:|
| 144:288 | 1012:1016 | 1020:1024 | 8 | 176 | 0,75 / 0,75 | 0,75 / 0,75 |
| 432:576 | 1016:1020 | 1024:1028 | 8 | 176 | 0,625 / 0,625 | 0,6875 / 0,6875 |

Cada perna contém quatro seeds, dois oponentes e dois assentos (16 partidas).
São nove pernas de busca (referência e oito variantes), mais duas pernas de check.
Os oponentes foram `clock::thomas_t95` e `clock::aberatozer_v23`, pelos caminhos
congelados no plano. A referência foi a fita 0 do yhay, sem seu roteador.
Todos os jogos terminaram sem falhas de callback. Nenhuma seed de validação ou
holdout foi consumida. Os checks são desenvolvimento disjunto dentro de cada
experimento, não validação competitiva independente certificada pelo registro.

## O que as variantes mostraram

As primeiras seis variantes substituem todos os `PASS` explícitos do bloco por
uma tarefa: regar, colher, cuidar, alimentar, coletar fertilizante ou fertilizar.
As duas seguintes trocam a ordem de tarefas estacionárias consecutivas.

No primeiro bloco, a referência teve 128 ações sem efeito nas 16 partidas de
busca. As seis variantes de preenchimento de `PASS` produziram entre 1.696 e
1.800. Substituir `PASS` por `HARVEST` aumentou dinheiro médio em 122,5 moedas,
mas não ganhou nenhuma partida adicional; a busca corretamente não aceitou a
mudança. Uma troca de tarefas reduziu o placar de 0,75 para 0,50 e foi rejeitada.
No segundo bloco, nenhuma variante melhorou o placar da referência.

Os checks deram delta zero porque o candidato congelado era a própria fita
original. Esse zero não é um teste de equivalência de todas as variantes; elas
foram descartadas na busca e não foram usadas para escolher pelo check.

## Reprodução e evidência

O comando do primeiro experimento está em [BLOCK_SOLVER.md](BLOCK_SOLVER.md).
Para o segundo, usar os mesmos argumentos com `--start 432 --days 6`,
`--seeds 1016:1020 --check-seeds 1024:1028 --workers 2` e outro diretório de saída.
Ambos usaram oito propostas, uma rodada e PRNG seed 771. Tempos observados:
87,83 s e 149,58 s, com testes e/ou outro experimento simultâneos; não representam
um benchmark controlado de desempenho.

[production-search.json](production-search.json) preserva planos, hashes de
partidas, mutações, diagnósticos e resultados. As listas extensas de alvos de
`idle_work` são representadas por contagem/hash nesse resumo; os detalhes completos
estão em `selection.json` nos diretórios locais `experiments/searches/production-144-01`
e `production-432-01`, junto das partidas e estados de chegada. Esses diretórios
são ignorados pelo Git. Os dois experimentos começaram antes da inclusão dos hashes
dos geradores no plano; planos de novas execuções já incluem esses hashes.

## Próxima hipótese

As tarefas propostas precisam considerar o estado observado do trabalhador e do
tile. Gerar trabalho sem verificar alvo, carga e recursos tende a produzir ações
sem efeito. A próxima etapa deve extrair oportunidades executáveis nas fronteiras
ou ao longo do bloco, gerar pequenas sequências coerentes e medir a continuação.
Não faz sentido ampliar apenas a quantidade de substituições cegas de `PASS`.

A #39 permanece aberta: ainda faltam uma biblioteca com melhoria demonstrada e
roteamento medido sobre variantes complementares. Esta entrega conclui a ampliação
do gerador e sua primeira avaliação, não o objetivo competitivo completo.
