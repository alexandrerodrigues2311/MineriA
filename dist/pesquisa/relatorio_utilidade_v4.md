# MinerIA — utilidade dos novos experimentos

Esta versão testa três usos distintos: priorizar revisão de áreas, descrever perfis administrativos e estimar lances. Todos os resultados são retrospectivos. A rodada 8 já havia sido examinada; não é um teste prospectivo independente.

## O que foi executado

Classificação supervisionada: HGB com atributos básicos, trajetórias e novos marcos; Extra Trees com marcos. Comparações com frequência histórica suavizada por UF e ordenação pela área. Alvos separados: lance positivo e resultado Livre. Seleção pela média do ganho de concentração no topo de 20% nas rodadas 4 e 5.

Treinamento/validação: rodadas 1–2 → 4; 1–3 → 5. Avaliação final: 1–5 → 8. Processos presentes na avaliação são removidos do treinamento. Os cortes dos eventos continuam anuais e conservadores; não se usa evento posterior ao corte. A área, o ano e a UF integram os atributos básicos. Substâncias, eventos, documentação, títulos e associações integram as versões enriquecidas.

Os novos marcos medem presença de registro de disponibilidade, quantidade de registros, dias desde o primeiro/último registro e contexto do evento anterior. Este contexto não certifica a fase jurídica. Ainda não equivale ao intervalo exato entre entrada em disponibilidade e abertura do edital.

Uma auditoria de cobertura encontrou marcos anteriores ao corte em 0/499 registros da rodada 1, 34/6.863 da 2, 26/2.748 da 3, 9/1.650 da 4, 7/4.465 da 5 e 3.167/4.950 da 8. A mudança de cobertura limita fortemente o aprendizado dessas variáveis. Ausência de marco registrado não significa ausência de disponibilidade. O enriquecimento não está completo apenas por acrescentar colunas.

## Priorização: que decisão pode apoiar?

O gestor escolhe quantas áreas a equipe consegue revisar. A pontuação organiza uma fila, sujeita a revisão humana; não é probabilidade calibrada nem autorização para excluir áreas. Maior concentração do alvo entre as primeiras áreas pode tornar a revisão mais dirigida.

| Alvo | Modelo escolhido | Precisão no topo 20% | Captura do total | Ganho sobre aleatório |
|---|---|---:|---:|---:|
| lance_positivo | hgb_basico | 79.5% | 24.1% | 1.21× |
| livre | extra_marcos | 32.5% | 32.1% | 1.60× |

### lance_positivo

Revisando 990 de 4950 áreas, a seleção contém 787 ocorrências do alvo. Foram observadas 65.9% no conjunto completo. Critério mínimo de lift >1,10 nas duas validações e na rodada 8: atendido.

| Método | Rodada 4: lift | Rodada 5: lift |
|---|---:|---:|
| hgb_basico | 2.18 | 1.57 |
| hgb_trajetoria | 2.15 | 1.56 |
| hgb_marcos | 2.15 | 1.56 |
| extra_marcos | 1.95 | 1.72 |
| frequencia_uf | 1.76 | 1.20 |
| regra_area | 1.96 | 1.04 |

Referências na rodada 8:
- frequencia_uf: precisão 81.3%; lift 1.23.
- regra_area: precisão 74.1%; lift 1.13.

Intervalo bootstrap de 95% para diferença de precisão frente à prevalência da rodada: 11.5 a 16.1 pontos percentuais. Reamostragem por processo, seleção fixa; não mede incerteza entre futuras rodadas nem inclui refazer a seleção de modelos.

### livre

Revisando 990 de 4950 áreas, a seleção contém 322 ocorrências do alvo. Foram observadas 20.3% no conjunto completo. Critério mínimo de lift >1,10 nas duas validações e na rodada 8: atendido.

| Método | Rodada 4: lift | Rodada 5: lift |
|---|---:|---:|
| hgb_basico | 1.31 | 1.31 |
| hgb_trajetoria | 1.49 | 1.34 |
| hgb_marcos | 1.44 | 1.36 |
| extra_marcos | 1.50 | 1.40 |
| frequencia_uf | 1.38 | 1.19 |
| regra_area | 0.62 | 1.10 |

Referências na rodada 8:
- frequencia_uf: precisão 33.0%; lift 1.63.
- regra_area: precisão 18.7%; lift 0.92.

Intervalo bootstrap de 95% para diferença de precisão frente à prevalência da rodada: 9.7 a 14.8 pontos percentuais. Reamostragem por processo, seleção fixa; não mede incerteza entre futuras rodadas nem inclui refazer a seleção de modelos.

## Agrupamento: perfis sem usar o resultado

KMeans e mistura gaussiana diagonal foram comparados com 3, 5 e 8 grupos. O KMeans agrupa por proximidade; a mistura gaussiana permite componentes com dispersões distintas. Os lances e destinos não entram no agrupamento. Logaritmos e padronização reduzem o domínio das escalas. A escolha usa separação interna, estabilidade e tamanho mínimo, definidos antes da execução.

Ajuste em 16223 processos únicos de rodadas anteriores, excluindo processos da rodada 8. Dez dimensões: área, idade, diversidade de eventos, dias observados, amplitude e intervalo do histórico, eventos recentes, documentação, associações e títulos vencidos.

| Configuração | Silhouette | Estabilidade ARI | Menor grupo |
|---|---:|---:|---:|
| kmeans_3 | 0.267 | 0.987 | 15.3% |
| kmeans_5 | 0.326 | 0.995 | 1.6% |
| kmeans_8 | 0.241 | 0.902 | 1.6% |
| gmm_3 | 0.438 | 0.881 | 4.4% |
| gmm_5 | 0.312 | 0.952 | 4.4% |
| gmm_8 | 0.220 | 0.800 | 1.6% |

Escolha: **gmm_3**. Silhouette mede separação; ARI compara a partição com cinco ajustes em amostras de 80%. Os limiares são critérios operacionais deste estudo, não certificação universal.

A estabilidade variou de 0.408 a 1.000. A média não deve esconder a reamostragem menos estável. Registros ausentes de documentação podem influenciar os perfis; ausência no banco não prova inexistência de documento.

| Perfil | Processos treino | Áreas rodada 8 | Idade mediana treino | Dias distintos treino | Lance positivo na rodada 8 | Livre na rodada 8 |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 715 | 855 | 13 | 18 | 71.5% | 16.7% |
| 2 | 2426 | 675 | 4 | 2 | 60.1% | 25.8% |
| 3 | 13082 | 3420 | 7 | 8 | 65.6% | 20.1% |

Os destinos acima são descrições posteriores: não serviram para escolher os grupos. Aplicação proposta: comparar carteiras com históricos semelhantes, distribuir revisões e investigar perfis pouco compreendidos. Os grupos não demonstram potencial geológico, causas de desinteresse ou identidades de participantes.

## Estimação do lance

Extra Trees escolhido com atributos **trajetoria**. Na rodada 8: RMSLE 1.858; erro absoluto médio R$ 164,639.78; R² -0.050. Se o erro continuar elevado e R² negativo, não recomendar uso para determinar lance ou receita.

## O que falta para demonstrar valor em uso

Um piloto com analistas deve comparar a fila do modelo com a prática atual, registrando tempo de revisão, achados úteis, áreas relevantes deixadas fora e concordância dos especialistas. Congelar o modelo e as previsões antes de nova rodada. Agrupamentos precisam receber interpretação dos especialistas e ter estabilidade acompanhada. Sem esse piloto, há evidência retrospectiva de organização da informação, não ganho operacional comprovado.

Os cortes anuais não incorporam todos os eventos imediatamente anteriores ao edital. A base atual pode conter revisões posteriores. Não há concorrência por área identificada de forma suficiente para modelar estratégias individuais. O trabalho ainda precisa de marcos de edital auditados e dados geológicos/territoriais historicamente válidos.

## Ciência aberta

Código, protocolo, dados derivados, resultados de todas as configurações e manifesto SHA-256 estão no pacote V4. O script reproduz a execução a partir da base congelada e dos históricos derivados; isso não equivale a refazer a extração dos arquivos brutos. O código usa scikit-learn 1.9.0 nesta versão, após restauração do ambiente, e refaz os controles V4 no mesmo ambiente. Não comparar diferenças mínimas com V3 como efeito isolado dos atributos.

Referências metodológicas: [agrupamento e medidas de avaliação](https://scikit-learn.org/stable/modules/clustering.html), [misturas gaussianas](https://scikit-learn.org/stable/modules/mixture.html). Fontes dos registros: [ANM SOPLE](https://dadosabertos.anm.gov.br/SOPLE/) e [Cadastro Mineiro](https://dadosabertos.anm.gov.br/SCM/).

## Auditoria adicional das referências

Com desempate aleatório esperado, a regra por UF alcança 81,39% para lance positivo e 32,91% para Livre, contra 79,49% e 32,53% dos modelos. A regra de menores áreas chega a 28,71% para Livre. Portanto, não há superioridade consistente de aprendizado supervisionado sobre a referência estadual no topo de 20%. Essa checagem posterior não trocou os modelos escolhidos.
