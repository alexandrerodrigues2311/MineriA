# MinerIA V5 — destinos da oferta

Experimento retrospectivo adicional, registrado antes da execução. A rodada 8 já foi examinada: não é teste prospectivo. Não alterar hiperparâmetros após observar o resultado final.

Objetivo: distinguir Arrematada, Conquistada e Livre, sem confundir lance positivo com qualquer destinação. Treinar 1–2 e validar em 4; treinar 1–3 e validar em 5; escolher pelo F1 macro médio; treinar 1–5 e avaliar em 8. Remover do treino números de processo presentes no teste; vínculos entre números diferentes ainda podem gerar dependência residual.

Comparar frequência global e frequência suavizada por UF com regressão logística, HistGradientBoosting básico, HistGradientBoosting com trajetória e ExtraTrees com trajetória. Parâmetros fixos no script. Não realizar busca interminável. Excluir identificadores e resultados dos atributos. Manter cortes históricos conservadores e dados congelados V4, sem acrescentar eventos posteriores.

Reportar F1 macro (peso igual aos três destinos), acurácia balanceada, log-loss, Brier multiclasses, matriz de confusão e precisão no topo de 20% por classe. Comparar a seleção com todas as referências, inclusive resultados desfavoráveis. Reamostragem pareada por processo, 300 repetições, para diferença de F1 macro frente à referência por UF; intervalo condicional a esta rodada e modelos fixos. Importância por permutação de famílias de atributos, cinco repetições: relevância preditiva, não significância nem causalidade.

Separar recortes estratégicos e alta tecnologia usando a classificação retrospectiva SGM/MME 2/2021. Não reclassificar automaticamente como lista vigente de minerais críticos. Substâncias usadas para definir o subgrupo provêm do cadastro atual e podem não ser conhecidas na época.

Simulador será reprodução da avaliação histórica, não recomendação automática para o estoque nem preço mínimo. Trajetórias e CFEM posteriores serão contexto separado e jamais atributos do modelo.
