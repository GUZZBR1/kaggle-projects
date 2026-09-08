# Para onde ir depois da #24: a abertura não tem fonte de receita

Derivado das 3.200 partidas já gravadas do torneio da #24, sem execução nova.
Comparação restrita às famílias neutras (`seyamalam_v21` e `lonespear_v11`),
para não medir o confronto direto entre os dois. 400 partidas de cada lado,
telemetria reconciliando integralmente nos dois casos.

## O número que explica o resto

| | v002 | cok_v10 |
|---|---:|---:|
| Primeira receita (passo) | **252** | **1** |
| Piso de caixa | 250,0 | 9,5 |
| Receita nos dias 0–2 | **0** | 382/partida |
| Dinheiro no dia 29 | 46.481 | 99.256 |

O `cok_v10` vende no **primeiro turno**. O `v002` espera 252 passos — dez dias
e meio — pela primeira venda.

O que ele vende cedo é específico e reproduzível: **FERTILIZER** (299/partida,
3 unidades) e **WHEAT** (82,5/partida, 3 unidades) nos três primeiros dias. O
`v002` vende exatamente nada no mesmo período.

## Por dia, o mecanismo

| dia | v002 caixa / mãos / receita | cok_v10 caixa / mãos / receita |
|---:|---:|---:|
| 0 | 506 / 7,67 / 0 | 17 / 4,79 / 82 |
| 3 | 297 / 3,83 / 0 | 10 / 4,67 / 394 |
| 6 | 250 / 1,92 / 0 | 1.706 / 3,83 / 2.994 |
| 9 | 250 / **0,00** / 0 | 2.018 / **11,12** / 2.351 |
| 10 | 1.775 / 0,00 / 3.544 | 17.413 / 10,25 / 17.132 |

O `cok_v10` opera com caixa mais apertado que o nosso (piso 9,5 contra 250) e
mesmo assim nunca fica insolvente, porque a receita entra todo dia. Ele usa
essa receita para **escalar mão de obra** — 11 trabalhadores no dia 9, quando o
`v002` está com zero — e chega ao dia 10 com 17.413 contra nossos 1.775.

Não é gestão de caixa melhor. É ter o que vender.

## Isso reinterpreta a rejeição do X-LIQ (#25)

O X-LIQ tratava os três primeiros dias de uma abertura centrada em cultura
lenta, e foi rejeitado pela evidência (score −0,875, todas as famílias
regrediram). Faz sentido: administrar melhor um caixa que não tem entrada não
cria entrada. O experimento não estava mal executado — a hipótese é que estava
endereçando o sintoma.

O alvo real é a **ausência de fonte de receita precoce**, não a curva de caixa.

## Próximo passo sugerido

Uma hipótese testável com a infraestrutura que já existe: dar à abertura um
produto vendável nos primeiros dias — fertilizante e/ou trigo, que é o que a
família dominante monetiza — e medir com o mesmo protocolo pareado da #25.
O critério de aceitação natural é primeira receita e piso de caixa, que a
telemetria diária já reporta, além do score por família.

Isto é uma direção sustentada por evidência, não uma decisão tomada. Nenhuma
mudança estratégica foi feita neste documento.
