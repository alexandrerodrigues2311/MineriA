# Ficha detalhada dos modelos — LanceMineral IA

## 1. Pergunta, unidade e tipo de aprendizado

O aprendizado é **supervisionado**: cada observação histórica tem um resultado conhecido, usado para ensinar o algoritmo. Não foi realizado agrupamento não supervisionado, não foi utilizado modelo de linguagem e não há sistema de recomendação de estratégia de leilão.

A unidade é uma combinação de rodada, área e processo. Quando a mesma área possui registro de oferta pública e de proposta fechada, prevalece o da proposta fechada. Há 21.175 observações comerciais elegíveis. Rodadas 6 (social), 7 (cancelada), retiradas e suspensas ficam na exploração descritiva, mas não no alvo comercial. Não se transformam cancelamentos em lances zero.

O problema foi dividido em dois:

1. **Classificação binária:** a área será arrematada? Alvo 1 para Arrematada com lance positivo e 0 para Livre/Conquistada. A saída é uma probabilidade experimental, não a chance de determinado minerador vencer.
2. **Regressão condicional:** se houver arrematação, qual o valor central do lance vencedor? Treinada apenas nos lances positivos. O alvo transformado é `log1p(lance)`, convertido de volta por `expm1`. Essa transformação reduz a influência da escala e privilegia o erro proporcional, não o erro em reais.

O valor central retornado após transformar a escala não equivale automaticamente à média monetária esperada. Multiplicar essa previsão pela probabilidade e somar áreas não produz, por si só, uma previsão validada de arrecadação. Também faltam pagamentos, inadimplência e conciliação financeira.

## 2. Variáveis explicativas realmente consideradas

### Conjunto básico — usado no classificador selecionado

| Variável | Construção | Ressalva |
|---|---|---|
| `uf` | Estado da área no registro da rodada | Composição da oferta muda entre rodadas |
| `regime` | Regime de disponibilidade informado | Conciliação com anexo original ainda necessária |
| `log_hectares` | `log1p(abs(área em hectares))` | Valor absoluto usado no código original; sinais anômalos precisam auditoria, não interpretação física |
| `ano_processo` | Ano extraído do número do processo | Ano não é prova de idade geológica nem valor econômico |

### Conjunto histórico — usado no estimador selecionado de lance

Inclui as quatro variáveis básicas e:

| Variável/família | Construção antes do corte |
|---|---|
| `eventos_anteriores` | Total de eventos com data anterior ao corte |
| `historico_ausente` | 1 quando não há evento anterior disponível |
| `evento_<código>` | Contagem de cada tipo de evento |
| `dias_ultimo_evento` | Dias desde o último evento anterior; campo ausente se não existe histórico |
| `titulos_publicados` | Total de títulos com publicação anterior |
| `titulo_<código>` | Contagem por tipo de documento legal |
| `substancias_historicas` | Número de substâncias com início de vigência anterior |
| `substancia_<código>` | Presença de cada substância já registrada antes do corte |
| `requerentes_titulares_historicos` | Número de pessoas distintas na relação de titular/requerente com início anterior; sem identidade como variável |

As substâncias históricas incluem qualquer registro iniciado antes do corte; não são uma reconstrução perfeita da substância vigente no edital. As identidades dos titulares não entram no modelo nem no pacote.

### Conjunto territorial — candidato e faixas retrospectivas

Acrescenta `associacoes_anteriores`, `municipio_ausente`, `cfem_sem_registro`, `cfem_log_3anos`, `dipem_sem_registro` e `dipem_log_3anos`. Os valores municipais são somados nos anos `ano_corte−4` a `ano_corte−2`, transformados por `log1p`. A ausência recebe indicador separado.

Os vínculos de município são os atuais. A base pública de investimentos em pesquisa mineral (DIPEM) começou a ser aberta depois da 8ª rodada; por isso, o candidato territorial e as faixas de quantis são diagnósticos retrospectivos, não previsões comprovadamente disponíveis à época. CFEM é contexto econômico municipal, não pagamento do leilão.

### Experimento adicional de mudanças entre rodadas

O script `round_changes.py` acrescenta tamanho da oferta, área mediana, concentração por estado, proporções dos regimes, quantidade média de eventos, participação da oferta no mesmo estado, idade do processo e índice IPCA conhecido antes do corte. O alvo positivo é ajustado para novembro de 2019 e depois reconvertido para a escala nominal.

A composição da oferta foi reconstruída do arquivo final atual e não de todas as versões dos anexos. Esse experimento apresentou AUC próxima de 0,707 e erro médio de R$ 162,9 mil na 8ª, mas **não substituiu o modelo principal**: ele usa contexto retrospectivo e informação cuja disponibilidade pública histórica não foi comprovada. Selecionar o melhor resultado depois de olhar o teste produziria otimismo indevido.

### O que não entrou

Número sequencial do processo, nome/CPF/CNPJ dos participantes, vencedor, lance observado da área avaliada, situação final como variável explicativa, eventos posteriores ao corte, geometria atual como preditor e estoque atual como se fossem dados históricos não entram no modelo principal. O número do processo serve para vínculo e remoção de sobreposição; apenas o seu ano vira variável.

O dicionário `variaveis_expandidas.csv` identifica todas as colunas codificadas no treino final. Categorias são transformadas em indicadores pelo `DictVectorizer`, ajustado somente no treino; categorias novas no teste são ignoradas. Campos numéricos ausentes no dicionário viram zero nessa representação. Isso é uma escolha de implementação, não ausência semântica garantida; em particular, a ausência de `dias_ultimo_evento` deve ser interpretada junto com `historico_ausente`.

Não foi calculada uma explicação causal nem um ranking validado de importância de variáveis. O fato de uma variável estar no modelo não demonstra que ela determina o lance. Importância por permutação e estabilidade entre rodadas são trabalhos pendentes; não foram inventados gráficos de importância.

## 3. Treino, escolha e teste temporal

| Etapa | Rodadas | Observações |
|---|---|---:|
| Treino para escolha | 1, 2, 3 | 10.110 |
| Validação para escolher | 5 | 4.465 |
| Reestimativa dos escolhidos | 1, 2, 3, 4, 5 | 16.223 |
| Avaliação retrospectiva | 8 | 4.950, sendo 3.260 arrematadas |

A 4ª rodada foi excluída do primeiro treino porque a homologação ocorreu depois da abertura da 5ª. Processos presentes na validação são retirados do treino de escolha. Processos presentes no teste são retirados do treino final, evitando que a mesma chave apareça dos dois lados.

Os cortes históricos conservadores são 01/01/2020 (rodadas 1 e 2), 01/01/2021 (3 a 5) e 01/01/2024 (8). Apenas datas estritamente anteriores são usadas. Não são as datas exatas de abertura de todos os editais. Uma informação com data de evento antiga, extraída em 2026, não está automaticamente comprovada como pública antes do leilão.

Foram comparadas seis combinações: Random Forest/histórico, Extra Trees/histórico, HistGradientBoosting/básico, HistGradientBoosting/histórico, regressão logística e Ridge/histórico, HistGradientBoosting/territorial. Sem busca extensiva de parâmetros. O classificador é escolhido pelo menor Brier na 5ª; o regressor pelo menor RMSLE entre lances positivos na 5ª.

Escolhidos: **HistGradientBoostingClassifier com variáveis básicas** e **RandomForestRegressor com variáveis históricas**. Semente 42. HGB: 150 iterações, até 15 folhas, regularização L2=10. Floresta: 180 árvores, profundidade máxima 12, pelo menos 12 observações por folha, fração de variáveis 0,7. Todos os demais parâmetros explícitos estão no código.

A 8ª já havia sido examinada no estudo inicial. Ela é avaliação temporal retrospectiva, **não teste prospectivo intocado**. Não houve validação externa, experimento em produção ou revisão independente concluída. A reprodução computacional é outra coisa: confirma se o código refaz os números, não se o modelo será útil no futuro.

## 4. Resultados e interpretação

| Indicador na 8ª rodada | Referência constante | Modelo selecionado V2 | Leitura |
|---|---:|---:|---|
| AUC | 0,500 | 0,657 | Discriminação moderada; não significa 65,7% de acerto |
| Brier | 0,381 | 0,314 | Erro de probabilidade menor que a referência, ainda sem calibração demonstrada |
| RMSLE | 2,143 | 1,944 | Redução de aproximadamente 9,3% do erro na escala logarítmica; não é erro percentual |
| Erro absoluto médio | R$ 168.349 | R$ 165.611 | Ganho monetário pequeno: aproximadamente 1,6% |

A referência de probabilidade é a proporção de arrematação no treino, e a de valor é a mediana dos lances positivos do treino. Nenhuma utiliza o resultado do teste para ajustar o valor constante.

O erro absoluto médio é calculado apenas nas 3.260 áreas arrematadas, comparando valor observado e previsto. Valores muito altos influenciam a média. A mediana observada dos lances positivos da 8ª foi aproximadamente R$ 31,6 mil; isso reforça a necessidade de analisar a distribuição dos erros, e não interpretar o MAE como erro típico de toda área.

O modelo V2 **não venceu todos os modelos em todas as métricas**: a floresta histórica inicial teve AUC de aproximadamente 0,665 e Brier 0,300 na mesma avaliação. A escolha V2 foi feita pela regra de validação na 5ª, não pelo melhor número encontrado depois de olhar a 8ª.

As faixas entre os quantis 10% e 90% deveriam, nominalmente, conter 80% dos valores. Cobriram apenas **62,3%** dos lances positivos na 8ª; são estreitas ou inadequadas para parte da mudança observada. Não são intervalos calibrados de segurança financeira, e usam variáveis territoriais retrospectivas.

## 5. Por que o desempenho muda

A proporção de áreas arrematadas passou de cerca de 26,3% nas rodadas 1–5 para 65,9% na 8ª. A mediana dos lances positivos aumentou de cerca de R$ 10,1 mil para R$ 31,6 mil. A composição da oferta também mudou. Essas diferenças de distribuição dificultam transferir relações históricas para outra rodada.

São muitas áreas, mas apenas seis rodadas comerciais. Dependências entre áreas, concorrentes e regras de um mesmo edital limitam a quantidade de evidência independente. Ainda não foram produzidos intervalos de confiança das métricas que respeitem essa estrutura. Um grande número de linhas não resolve a escassez de rodadas independentes.

## 6. Usos permitidos pela evidência atual e próximos critérios

Uso atual sustentado: conferir resultados, identificar lacunas, comparar perfis e formular hipóteses; usar o modelo como referência experimental auditável. Uso ainda não sustentado: recomendar o lance ótimo, estimar reservas, atribuir causalidade, comprometer orçamento ou projetar receita recebida com confiabilidade demonstrada.

Antes de uso operacional: preservar anexos e bases conhecidos antes da abertura; registrar previamente as regras de seleção; validar em rodada nova sem reajustar no teste; comparar referências fortes por substância/região; calibrar probabilidades e faixas em dados separados; analisar erros por valor, estado, substância e grupo de processos; avaliar estabilidade e incerteza entre rodadas; conciliar lances com pagamentos e inadimplência; definir um critério de benefício econômico com os usuários.

Não se promete atingir uma métrica específica. As hipóteses podem não se confirmar. Um artigo defensável deve relatar também resultados negativos, mudanças de escopo e limitações de disponibilidade histórica, sem vender esta etapa como solução preditiva pronta.
