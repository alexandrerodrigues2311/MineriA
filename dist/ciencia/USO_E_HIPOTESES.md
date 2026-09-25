# MinerIA — perfis, hipóteses e uso prático

## Indicadores e território

Os tooltips explicam a unidade área por rodada, a distinção entre áreas arrematadas, conquistadas e livres e entre lances registrados e pagamentos. O mesmo processo pode reaparecer. Poligonais da ficha são atuais do SIGMINE; mapa geral mostra estados e mapa de exploração mostra pontos representativos. Não existe reconstrução automática da poligonal de cada edital.

A tabela municipal usa vínculos da área no resultado da rodada. Uma área associada a vários municípios conta uma vez em cada município; o lance é dividido igualmente entre os municípios listados. O rateio serve somente para análise, não mede arrecadação municipal ou proporção territorial.

## Participantes e vencedores

InteressadoParticipante.csv informa rodada, modalidade, nome, documento mascarado, município e UF. Não contém chave da área ou lance individual. ResultadoRodadaDisponibilidade.csv contém vencedor e lance vencedor por área. As fases são consolidadas pela chave rodada, número de área e processo, preferindo proposta fechada; apenas Arrematada entra na estatística de vencedores comerciais.

Os cadastros são agrupados por nome normalizado (caixa alta e espaços) e documento mascarado sem pontuação. São aproximações, não identidades verificadas: grafias diferentes e colisões de máscaras afetam contagens. Não se reconstituem documentos. PF/PJ é inferido do número de posições do formato mascarado (11/14), com categoria de ausência. Nomes dos estados são convertidos às siglas; municípios têm caixa e espaços normalizados, sem associação aproximada a códigos IBGE. Ausência é exibida como Sem registro.

Contagens por modalidade e município são registros, não pessoas únicas; um cadastro pode aparecer mais de uma vez. Cadastros únicos usam a chave declarada. Concentração financeira agrega lances por cadastro vencedor; não equivale a grupo econômico nem à concentração de todos os concorrentes. A soma das áreas vencedoras e dos lances é reconciliada com a visão geral (7.528 e R$ 907.604.126,29 nesta extração). A visualização contém somente agregados, sem nomes ou documentos.

Lances perdedores, manifestações por área e datas de entrada são necessários para estimar competição ou taxa individual de vitória. Os perfis novos são descritivos; não foram incorporados ao treinamento existente. Um futuro preditor de experiência deve usar apenas participação anterior ao corte, com identidade validada e regras de disponibilidade da informação.

## Seis configurações supervisionadas

As três linhas da comparação principal são referência constante, experiência inicial e seleção V2; não são três únicos candidatos. Foram seis configurações, cada uma com classificação e regressão:

| Configuração | Hipótese e diferença |
|---|---|
| Random Forest / histórico | A média de árvores captura interações e reduz instabilidade; eventos e títulos anteriores acrescentam sinal. |
| Extra Trees / histórico | Cortes mais aleatórios podem reduzir sobreajuste mantendo o conjunto informacional. |
| HistGradientBoosting / básico | UF, regime, log da área e ano do processo podem bastar para parte da procura. |
| HistGradientBoosting / histórico | Comparação com boosting básico isola o ganho do conjunto histórico dentro do mesmo algoritmo. |
| Logística e Ridge / histórico | Relações aditivas regularizadas podem generalizar com menor complexidade. |
| HistGradientBoosting / territorial | Contexto de CFEM/DIPEM pode acrescentar informação; DIPEM e vínculos atuais limitam a interpretação à retrospectiva. |

Hipóteses são preditivas, sem inferência causal ou teste de significância confirmado. Escolha pela 5ª rodada: menor Brier seleciona boosting básico para ocorrência; menor RMSLE seleciona floresta histórica para lance. A ficha principal descreve parâmetros, variáveis, cortes, exclusões e métricas. Não houve busca exaustiva; outros algoritmos não foram demonstrados inferiores. Aumentar candidatos após observar a 8ª aumenta o risco de selecionar ruído. Novas comparações precisam de protocolo temporal e teste prospectivo previamente reservado.

O modelo de quantis testa a dispersão, mas cobertura nominal de 80% chegou a 62,3%. O experimento de contexto de rodada testa diferenças de composição/regras e IPCA; é retrospectivo e não substitui o modelo escolhido. Nenhum foi convertido em recomendação de lance.

## Simulador retrospectivo

Usa as 4.950 previsões congeladas da 8ª rodada, não realiza treinamento ou nova inferência. Filtros: estado, regime, área mínima e limiar de probabilidade. Seleciona quando p >= limiar. Mostra quantidade encaminhada, proporção arrematada entre encaminhadas, fração de arrematações recuperadas e arrematações deixadas de fora. Denominadores vazios são Não se aplica. O CSV contém todos os registros selecionados e o limiar usado.

No cenário geral com 50%: 1.018 áreas selecionadas, 810 arrematadas, 208 não arrematadas e 2.450 arrematações deixadas de fora. Isso é retrospectivo e não demonstra benefício operacional futuro. O total monetário mostrado é observado, não previsão nem ganho causado pelo filtro. O regressor produz um centro na escala logarítmica; somar p × valor não estima automaticamente receita esperada.

Para usar em nova rodada, é preciso construir características apenas com informação previamente disponível, congelar o conjunto antes de resultados, aplicar os modelos, calibrar usando validação anterior e avaliar a nova rodada sem seleção posterior. Valoração econômica, reservas, custos, pagamentos e inadimplência não estão modelados. O protótipo atual apoia consulta e pesquisa; o uso decisório das previsões requer essa validação.

## Desempenho e reprodução

build_delivery.py gera metadata.json, overview-summary.json, areas.json e participants.json a partir dos snapshots originais. Os dois primeiros carregam na entrada (169.605 bytes nesta versão, ante 21.230.675 bytes nas três bases previamente antecipadas). Trata-se do volume bruto de JSON, não benchmark de tempo hospedado. Áreas: 6.399.842 bytes, sob demanda; características e detalhes também carregam quando necessários. O código preserva toda a base; não retreina modelos.

O arquivo build_delivery.py está em codigo_original, os agregados de participantes e o relatório de verificação estão em dados. O código da interface e o simulador estão em interface/decision.js. Para regenerar agregados, disponibilize as fontes nos caminhos esperados pelo script, executando antes a integração original. Fontes: https://dadosabertos.anm.gov.br/SOPLE/ . A rotina diária foi atualizada para regenerar os novos arquivos após mudanças de dados.
