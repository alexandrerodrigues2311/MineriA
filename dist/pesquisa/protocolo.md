# MinerIA — protocolo fixado antes dos ajustes V3

Data: 25/09/2026. Estudo retrospectivo; a rodada 8 já foi examinada em versões anteriores. Não é teste prospectivo intocado. Não se otimizará o resultado da rodada 8.

## Decisão e alvos
Antes da oferta: ordenar áreas para análise humana pela probabilidade de arrematação e estimar o centro da distribuição do lance positivo. Lance vencedor consolidado não é pagamento, receita realizada, valor econômico da jazida nem lance ótimo. O segundo alvo só existe entre arrematações. Modelo multiclasse complementar distingue Livre, Conquistada e Arrematada.

## Reconstrução
Preservar todas as linhas de fase do SOPLE, incluindo retiradas/suspensões. Reconstruir eventos, títulos, relações, substâncias, documentação e associações do Cadastro Mineiro. Ordenar por data e código, sem inventar sequência intradia. Transições são entre eventos registrados, não estados jurídicos inferidos. Relação 8 é Disponibilidade; direção semântica e continuidade precisam ser conferidas antes de chamar associado de sucessor. Relação 12 (participante) deve ser auditada, não presumida disponível. Identidades de vencedores/participantes e observações livres não entram no modelo.

## Cortes e validação
Mantêm-se cortes conservadores anuais: 1/2 antes de 2020; 3/4/5 antes de 2021; 8 antes de 2024. São cortes dos atributos históricos, não datas de abertura. O banco atual não comprova quando cada registro se tornou público. Atributos de oferta vêm do resultado atual, sujeitos a revisão; isso limita inferência ex ante.
Validação A: rodadas 1/2 → 4, pois a rodada 3 não estava homologada na abertura da 4. Validação B: 1/2/3 → 5, excluindo 4, homologada posteriormente. Remover do treino todo processo presente na respectiva validação. Selecionar pela média simples entre as duas rodadas, sem deixar a maior dominar. Treino final 1–5 → avaliação 8, removendo processos sobrepostos. Não dividir linhas aleatoriamente.

## Bateria finita e hipóteses
H1: atributos básicos (UF, regime, área, ano) contêm sinal; H2: tipos de eventos e substâncias melhoram previsão; H3: recência, intensidade, intervalos, diversidade e mudanças administrativas agregam informação. Comparar HGB básico, HGB histórico, HGB trajetória, Random Forest trajetória, Extra Trees trajetória, logística/Ridge trajetória. Parâmetros fixos e semente 42. Referências: frequência histórica para probabilidade e mediana dos lances positivos para preço.
Classificação: selecionar por Brier (menor melhor), reportar AUC, perda logarítmica, precisão média, curva de calibração e captura em 10/20/50% da fila. Regressão: selecionar por RMSLE; reportar MAE, mediana do erro absoluto e R², sem esconder cauda monetária. Nenhuma seleção por teste 8.
Importância por permutação de grupos no teste 8 será explicação retrospectiva, não seleção nem significância estatística ou causalidade. Incerteza: reamostragem pareada por processo dentro de 8; não representa incerteza entre rodadas. Modelo multiclasse secundário com configuração fixada HGB trajetória, reportando log loss, acurácia balanceada e matriz de confusão.

## Critérios de uso
Ganhos frente à referência são necessários, mas não suficientes para produção. Instabilidade entre rodadas, probabilidades mal calibradas e grandes erros em reais restringem o uso a triagem assistida. Não publicar previsão de arrecadação ou recomendação de lance individual. Cenários de seleção mostram a troca entre quantidade revisada e arrematações históricas capturadas, não efeito causal de intervenção. Uma futura rodada, congelada antes do resultado, será a validação prospectiva necessária.

## Prêmio
Critérios do item 7.1: correção, adequação ao tema, objetividade, criatividade, inovação e aplicabilidade. Não há pesos nem fórmula 0–10 divulgada no edital examinado. Qualidade será auditada por evidência, sem atribuir nota da banca. Artigo anônimo, pseudônimo até 20 caracteres, 10–20 laudas textuais, A4 fonte12, resumo e abstract conforme edital. A elegibilidade e a submissão são do candidato.
