# Política de submissão final — issue #37

Verificado em 8 de setembro de 2026. O Bradley–Terry final usa episódios de toda a
competição, desde que ambos os agentes da partida continuem ativos. Não usa apenas
as partidas posteriores ao prazo. A explicação direta dos hosts resolve a
ambiguidade da expressão “those episodes” na página de avaliação.

## Fontes confirmadas

| Fonte | Autoridade e achado |
|---|---|
| [Tópico 732931](https://www.kaggle.com/competitions/kaggriculture/discussion/732931) | Addison Howard, Kaggle Staff, afirma que o ajuste usa episódios entre agentes ativos de toda a competição. Partidas contra agentes depois desativados deixam de contar. |
| [Resposta no mesmo tópico](https://www.kaggle.com/competitions/kaggriculture/discussion/732931) | Bovard Doerschuk-Tiberi, Kaggle Staff, confirma: “BOTH agents need to still be active for the episode to count”. |
| [Tópico 739410](https://www.kaggle.com/competitions/kaggriculture/discussion/739410) | Addison Howard confirma que a equipe recebe a pontuação da melhor das duas submissões; a segunda funciona como alternativa. “Ties are counted as half wins for each side.” Não há compromisso de quantidade ou frequência de episódios após o prazo. |
| [Avaliação e FAQ](https://www.kaggle.com/competitions/kaggriculture/overview/evaluation) | Limite de cinco submissões diárias e duas mais recentes ativas. Prazo em 30/09/2026, 23:59 UTC; jogos adicionais previstos de 01/10 até aproximadamente 15/10, sujeitos à convergência e ajustes dos organizadores. |

A resposta de Addison no tópico 732931 especifica o alcance temporal como
“across the whole competition”. Portanto o histórico anterior ao prazo pode
contribuir, mas depende também da sobrevivência dos adversários enfrentados.
Não basta contar os episódios totais de uma submissão para saber quanta evidência
vai permanecer no ajuste final.

As três pistas originais da issue foram verificadas:

- [736219](https://www.kaggle.com/competitions/kaggriculture/discussion/736219):
  é uma análise de participante; sua interpretação de avaliação somente após o
  prazo não prevalece sobre a resposta direta do host.
- [737788](https://www.kaggle.com/competitions/kaggriculture/discussion/737788):
  trata de uso de agentes públicos, não da população de episódios do ajuste.
- [738837](https://www.kaggle.com/competitions/kaggriculture/discussion/738837):
  trata do uso de replays públicos para construir agentes, não do Bradley–Terry.

## Política derivada para este projeto

Os itens abaixo são decisões locais baseadas nas regras, não exigências adicionais
dos hosts.

1. **Preservar o melhor agente comprovado.** Antes de qualquer envio, listar as
   duas submissões ativas em ordem cronológica e identificar qual será removida.
   Os slots funcionam por recência: não é possível prometer manter indefinidamente
   o melhor antigo e fazer vários testes no outro slot. A próxima submissão pode
   expulsar justamente o melhor.
2. **Usar as duas posições com alternativas fortes.** Não há benefício demonstrado
   em deixar uma posição vazia. A equipe recebe a melhor pontuação das duas, mas
   isso não torna uma substituição gratuita: a nova entrada desloca um histórico.
3. **Reservar duas das cinco oportunidades diárias para recuperação** em dias de
   envio planejado, deixando no máximo três para mudanças previamente aprovadas.
   Não são dois slots ativos extras e não há acúmulo de quota entre dias.
4. **Não reenviar o mesmo arquivo só para tentar um rating inicial melhor.**
   Isso perde o histórico da identidade anterior e não altera a política jogada.
   Uma melhoria incremental pode justificar troca se passar pelo gate local,
   preservar a alternativa mais forte e compensar o custo de perder evidência.
   “Mais episódios” sozinho não torna um agente inferior preferível a um superior.
5. **Planejar a última troca até 29/09/2026, 23:59 UTC**, deixando cerca de 24 horas
   para verificar carregamento, episódios reais e recuperar falhas antes do prazo.
   É uma margem operacional, não um ótimo estatístico demonstrado. Revalidar o
   cronograma oficial antes de agir e não depender de uma quantidade presumida de
   jogos após o prazo.
6. **Exigir gate competitivo e preflight do arquivo exato.** Registrar hashes,
   IDs dos dois agentes ativos, qual seria desativado, quota diária restante e
   motivo da substituição. Decidir olhando o resultado fora de espelhos e famílias
   compartilhadas. O gate local não conhece automaticamente o estado da conta Kaggle.

Ainda não foi confirmado se ratings correntes são usados como prior no ajuste,
qual é o cronograma exato de partidas após o prazo ou o tratamento dos slots quando
um upload falha em validação. A política não depende de respostas presumidas:
preflight antes de enviar, margem para recuperação e nenhuma troca automática.

## Rastreabilidade

`final-submission-sources.json` registra URLs, data de acesso, hashes SHA-256 das
extrações e os fatos confirmados. Os trechos curtos estão neste documento. As cópias integrais de navegação ficam no
cache local `.firecrawl/`; não são reproduzidas no repositório. Nenhuma mensagem
foi enviada aos hosts e nenhuma submissão foi feita para esta pesquisa.
