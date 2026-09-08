# `sell_lead` não é o que eu medi: era desempate de espelho

Correção de um achado que reportei nesta sessão. O número estava certo; a
interpretação estava errada, e ela mudaria a direção do projeto se ficasse de pé.

## O que eu tinha reportado

Ablação aditiva sobre o chassis v23, 120 e depois 160 partidas: partindo de
todas as camadas desligadas, ligar **só** `sell_lead` levava o agregado de 0,625
para 0,794 e o confronto com o `thomas95` de 0,500 para 0,838. As outras sete
camadas não mediam nada. Concluí que `sell_lead` era a camada que carregava o
chassis inteiro e que valia implementá-la.

## O que realmente estava acontecendo

Implementei a camada no nosso `tape_portfolio.py` e o pareado deu **+0,000** em
todas as cinco famílias, com as pontuações idênticas dígito a dígito. Isso não é
resultado nulo plausível — é sinal de que algo não roda. Fui atrás.

A camada não disparava por um bug meu (eu projetava só o galpão, ignorando os
depósitos do próprio turno). Corrigi. Continuou +0,000. Aí instrumentei o v23
original: o `_sell_lead` dele adiciona **3 ordens por partida**. Três ordens não
viram 27 partidas em 160.

O A/B direto explica tudo:

| | nosso | adversário | diferença | score |
|---|---:|---:|---:|---:|
| v23 sem camadas vs `thomas_t95` | 80.635 | 80.635 | **0** | 0,5 |
| v23 só com `sell_lead` vs `thomas_t95` | 80.635 | 80.634 | **+1** | **1,0** |
| v23 sem camadas vs `kaitofukami_v48` | 86.147 | 69.886 | +16.261 | 1,0 |
| v23 só com `sell_lead` vs `kaitofukami_v48` | 86.147 | 69.886 | +16.261 | 1,0 |

O v23 sem camadas **é** o `thomas_t95`: mesmas fitas, rota base, nenhuma
modificação. Contra o próprio doador ele empata exatamente, moeda a moeda. O
`sell_lead` ganha esse empate por **uma moeda** e converte 0,5 em 1,0. Contra um
adversário que não é clone, ele não muda absolutamente nada.

A ablação inteira estava medindo **qual perturbação ganha o desempate do
espelho**, não valor estratégico. Isso também explica por que `room_guard` (0,450)
e `dead_stock` (0,475) apareceram *piores* que o `bare` (0,500): perturbar um
empate pode cair para qualquer lado, e essas caem contra.

## O que sobrevive e o que cai

**Cai:** "`sell_lead` é a camada que carrega o chassis" e "`sell_lead` sozinho
bate as oito juntas". Ambas eram o mesmo artefato.

**Sobrevive:** o v23 completo realmente vence o `thomas95` com margens reais —
13 de 24 partidas, margens de centenas de moedas, só 2 de 24 dentro de 10
moedas. A força dele não é desempate. Mas ela não está no `sell_lead`.

**Explica:** por que a implementação correta não fez nada pelo `v003`. O `v003`
roteia entre `SCHEDULES[3]` e `[1]`, não é clone do `thomas95`, e perde para ele
com margem real (0,250). Não há empate para desempatar. Além disso a camada nem
dispara nas nossas fitas: elas vendem no primeiro instante possível — a
mercadoria está no inventário do farmer e ele vende no turno em que chega ao
galpão, sem folga para antecipar.

## A lição de método

**Medir um agente derivado contra o doador dele produz partidas espelho**, e num
placar de vitória/derrota qualquer perturbação de uma moeda vira uma vitória
inteira. O `worst family` ficou dominado por isso justamente porque o pior
adversário era o doador.

Quando um candidato compartilha fitas com um adversário do painel, empate exato
tem que ser tratado como categoria própria, não como derrota nem vitória. Vale
inspecionar a distribuição de margens antes de aceitar qualquer efeito: duas
linhas de diagnóstico teriam poupado o caminho todo.

## Estado do código

A implementação fica, correta e testada, com `lead_sale` ligado por padrão. Ela
não custa nada, não dispara nas nossas fitas hoje, e num ladder onde muita gente
roda o mesmo notebook público um desempate a favor tem valor real — mas é isso
que ela é, e o docstring agora diz isso.

---

> **Adendo (2026-09-08).** A retratação acima continua correta para as *nossas*
> fitas, e pelo motivo que ela dá: elas vendem no primeiro instante possível, então
> não há folga para antecipar e o único efeito observável era ganhar o empate do
> espelho por uma moeda.
>
> Nas fitas do `yhay81/shop-router-0908` há folga, e a camada vale de verdade. Em
> 25 seeds do split `validation`, sete famílias, dois assentos, 350 partidas por
> perna, ligá-la melhora **todos** os oponentes em placar e em margem, e o
> confronto direto contra o doador é 0,960 com **2 059 moedas** de margem média —
> não uma moeda. Ver `docs/V004_ONE_LAYER.md`.
>
> A lição de método deste documento é o que permitiu distinguir os dois casos:
> olhar a distribuição de margens antes de aceitar o placar. Ela não muda; muda
> apenas a conclusão sobre a camada, que agora depende da fita em que ela roda.
