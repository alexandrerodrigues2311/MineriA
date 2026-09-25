# MinerIA V5 — destinos e utilidade

Modelo escolhido nas validações 4 e 5: hgb_trajetoria. Treino final: 16223 áreas; avaliação retrospectiva: 4950 áreas na rodada 8.

Alvo supervisionado: Arrematada, Conquistada ou Livre. Corrige a ambiguidade anterior: lance positivo não inclui conquista sem disputa financeira.

F1 macro: 0.384, contra 0.174 da referência por estado. Acurácia balanceada: 42.5%. Log-loss: 0.959. Intervalo bootstrap pareado da diferença em F1: [0.19856237025971366, 0.2234514556576424].

| Objetivo | Precisão no topo 20%, modelo | Referência por UF | Frequência na rodada |
|---|---:|---:|---:|
| Arrematada | 83.9% | 81.3% | 65.9% |
| Conquistada | 17.4% | 9.0% | 13.9% |
| Livre | 33.8% | 33.0% | 20.3% |

O modelo concentra arrematações melhor que a referência por UF nesta avaliação (831 contra 805 em 990 áreas). O ganho não comprova uso prospectivo. A identificação categórica de Conquistada continua fraca: apenas 16 dos 686 casos foram classificados corretamente. Não há justificativa para implantação autônoma.

## Recortes minerais

- estrategico: 1875 áreas; F1 macro 0.429 vs 0.202; topo de arrematações 92.8% vs 92.3%.
- alta_tecnologia: 795 áreas; F1 macro 0.430 vs 0.204; topo de arrematações 88.1% vs 92.5%.

Alta tecnologia: a referência por UF ainda supera o modelo no topo de arrematações. Não generalizar a melhoria global a todos os subgrupos.

## Variáveis e interpretação

- UF: queda média de 2.15 pontos percentuais no F1 ao permutar.
- Área: queda média de 1.67 pontos percentuais no F1 ao permutar.
- Ano do processo: queda média de -0.08 pontos percentuais no F1 ao permutar.
- Regime: queda média de -0.24 pontos percentuais no F1 ao permutar.
- Histórico administrativo: queda média de 3.28 pontos percentuais no F1 ao permutar.

Importância preditiva não é efeito causal nem teste de significância. Atributos correlacionados podem compensar uns aos outros.

## Limitações
- Rodada 8 previamente examinada; não é validação prospectiva.
- Atributos congelados V4; cortes anuais e cobertura de eventos desigual.
- Processos excluídos por número; associações entre números diferentes ainda podem atravessar cortes.
- Agrupamento mineral retrospectivo; não é classificação atual de minerais críticos.
- Pontuações não calibradas para novas rodadas; não estimam preço mínimo.

O F1 macro novo não é comparável diretamente à precisão binária V4. Resultados foram obtidos com protocolo fixo, sem busca posterior de hiperparâmetros.

## Reprodução
Instale as versões do requirements-v5.txt. Execute python work/experiment_v5.py a partir da raiz do pacote. O script preserva o congelamento dos atributos e registra hashes. O pacote inclui apenas os campos necessários do SOPLE para classificar substâncias. Não inclui identificadores pessoais de participantes. Os relatórios históricos permanecem preservados.