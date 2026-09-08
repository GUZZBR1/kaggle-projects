# Emendar blocos: a distância diz *se* a junção é grátis, não *quanto* custa

`experiments/tape_splice.py` pontua o estado que um prefixo entrega ao bloco
seguinte. Este documento diz o que essa pontuação prevê e o que ela não prevê.

## Retratação do primeiro resultado

A primeira medição reportou **correlação −0,938** entre distância e perda, em 36
emendas, e concluiu que a distância serviria como filtro de busca por ordenação.

Isso estava errado por confundimento. As 36 emendas agrupavam três cortes com
escalas de perda muito diferentes: o corte 432 tinha distância alta *e* perda
alta, o 144 tinha as duas baixas. A correlação media majoritariamente o efeito do
**corte**, não o da distância. Era uma seed, um adversário, um assento e quatro
fitas do mesmo doador.

## A medição maior

Oito fitas de **duas procedências** (4 do `thomas_t95`, 4 do `yhay_router_0908`),
todas as 56 emendas cruzadas em dois cortes, 3 seeds, dois assentos, 720
partidas, zero falhas. Correlação dentro de cada corte:

| grupo | corte | n | correlação |
|---|---:|---:|---:|
| procedências diferentes | 144 | 192 | +0,109 |
| procedências diferentes | 288 | 192 | −0,088 |
| mesmo doador | 288 | 144 | −0,300 |
| todos | 144 | 336 | −0,299 |

**A ordenação por distância não sobrevive.** Entre procedências diferentes, que é
o caso que interessa para montar biblioteca, ela não prevê nada.

## O que sobrevive, e é o que serve

A pergunta útil não é "quanto custa" e sim "custa alguma coisa":

| corte | distância | n | perda mediana | fração com \|perda\| ≤ 50 |
|---:|---|---:|---:|---:|
| 144 | **= 0** | 108 | **0** | **100%** |
| 144 | > 0 | 228 | −377 | 16% |
| 288 | **= 0** | 36 | **0** | **100%** |
| 288 | > 0 | 300 | −4.585 | 1% |

**Distância exatamente zero prevê junção gratuita em 144 de 144 casos**, nas duas
procedências e nos dois cortes. Distância positiva quase nunca é gratuita —
1% no corte 288.

Ou seja: a pontuação é um **classificador de intercambiabilidade**, não um
estimador de custo. Isso é o suficiente para o que ela precisa fazer. Para montar
uma biblioteca de blocos o que se quer é justamente o conjunto de blocos que se
substituem sem custo — o grafo de compatibilidade — e não uma estimativa de quão
ruim é uma emenda ruim.

## Como usar

Trate `distance == 0` como "intercambiável" e qualquer coisa acima disso como
"precisa ser jogado para saber". Não ordene candidatos pela distância: entre
duas emendas caras, a maior distância não é a pior.

## Limites que continuam de pé

Duas procedências, dois cortes, um adversário (`kaitofukami_v48`), 3 seeds. O
limiar zero é exato e não tem tolerância ajustada — vale checar se uma tolerância
pequena (por exemplo `< 0,005`) mantém os 100% e amplia a cobertura, porque hoje
só 43% das emendas no corte 144 e 11% no 288 caem no conjunto gratuito.
