# MinerIA — Inteligência para a Gestão de Leilões Minerais

Versão de pesquisa: 24 de setembro de 2026. Projeto independente, desenvolvido com dados abertos da ANM. Identidade visual baseada no logo indicado pelo usuário e no pacote gov.br Design System 3.7.0. Não é um serviço oficial da Agência.

## 1. Finalidade

O MinerIA reúne exploração de resultados, histórico administrativo, localização e experimentos de aprendizado de máquina para apoiar decisões sobre a disponibilidade de áreas minerais. A aplicação permite avaliar onde houve interesse, como a composição das ofertas mudou e quais limitações impedem transformar uma estimativa em decisão de orçamento ou de lance.

O produto entrega uma base relacional, um painel interativo e experimentos reproduzíveis. Não entrega uma avaliação de reservas, viabilidade econômica, licenciamento, lance ótimo ou receita efetivamente recebida.

## 2. Escopo efetivamente integrado

Foram lidos integralmente os arquivos SOPLE de estoque, resultados por fase, participantes e avaliação social. O estoque contém 149.362 processos. A tabela de resultados comerciais/cancelados tem 31.841 linhas antes da consolidação das fases. O arquivo social acrescenta 420 linhas.

Após a consolidação por rodada, área e processo, há 26.516 observações nas oito rodadas e 23.554 processos distintos. Desses processos, 23.552 foram associados ao Cadastro Mineiro: 339.982 eventos, 57.929 relações de pessoas, 20.561 títulos, 28.029 relações de substâncias, 27.314 vínculos municipais, 9.754 associações, 168.776 registros documentais e 19.369 relações de propriedade do solo. Os números de relações não equivalem ao número de processos.

As camadas SIGMINE de ativos e inativos forneceram poligonais atuais para os 23.554 processos desse universo. A interface carrega a geometria e a sequência completa de eventos sob demanda. Não publica textos livres de eventos, nomes de vencedores, CPF/CNPJ ou identidades dos participantes.

CFEM e DIPEM foram integradas como contexto municipal histórico. O IPCA mensal foi obtido do SGS/BCB, série 433. Isso não significa que todas as bases do catálogo da ANM tenham sido integradas: produção individual, geologia detalhada, infraestrutura, restrições ambientais e pagamentos conciliados dos leilões ainda não compõem o modelo.

## 3. Como navegar

**Visão geral:** apresenta áreas por rodada, processos distintos, arrematações e soma de lances. O fluxo é interativo: clique no universo, nos resultados comerciais ou em um desfecho para abrir a seleção correspondente. Trata-se de um fluxo de destinação com ramificações, não de uma sequência causal de vendas.

**Explorar áreas:** combine rodada, UF e município. Os botões de resultado permitem filtrar com um clique. “Outras situações” inclui retiradas, suspensões, cancelamento e resultados sociais. A busca livre aceita número de processo com ou sem pontuação, município e substância. Os processos são exibidos no formato `000.000/0000`.

**Ordenação:** a tabela de áreas ordena toda a seleção antes de paginar, por processo, localização, substância, situação ou lance. As tabelas de resumo e modelos também permitem alternar a ordem pelos títulos das colunas. A exportação CSV acompanha os filtros ativos.

**Ficha:** contém a poligonal atual, controles de ampliação e deslocamento, a situação na rodada, o valor registrado e a lista completa de eventos disponíveis. A busca de eventos aceita código, descrição ou data. É possível alternar entre mais recentes e mais antigos. A situação “Livre” em uma rodada passada não confirma disponibilidade jurídica hoje.

**Entre rodadas:** apresenta composição e resultados, mudanças documentadas e um experimento adicional com contexto de oferta e inflação.

**Avaliação dos modelos:** mostra referências, critérios de seleção, erros e cobertura das faixas. Esses indicadores correspondem ao experimento congelado, não à seleção corrente do usuário.

## 4. Contagens e prevenção de dupla contagem

| Rodada | Áreas na base consolidada | Comerciais válidas | Arrematadas | Soma dos lances (R$) |
|---|---:|---:|---:|---:|
| 1 | 502 | 499 | 54 | 1.740.946,51 |
| 2 | 7.027 | 6.863 | 1.817 | 150.843.518,45 |
| 3 | 2.762 | 2.748 | 855 | 64.489.149,00 |
| 4 | 1.658 | 1.650 | 472 | 33.961.315,00 |
| 5 | 4.500 | 4.465 | 1.070 | 84.535.544,00 |
| 6 | 420 | Não se aplica | Não se aplica | Não se aplica |
| 7 | 4.647 | Não se aplica | Não se aplica | Não se aplica |
| 8 | 5.000 | 4.950 | 3.260 | 572.033.653,33 |

O total comercial é de 21.175 observações válidas, 7.528 arrematações e R$ 907.604.126,29 em lances vencedores registrados. O universo comercial também tem 4.583 áreas conquistadas e 9.064 livres. Os 5.341 registros restantes pertencem à rodada social, ao edital cancelado ou a situações excluídas do alvo comercial.

Essas são contagens do retrato atual dos arquivos, não uma certificação dos anexos originais de cada edital. A segunda rodada, por exemplo, teve quantidade divulgada em notícia oficial diferente do total atual consolidado; não se deve ocultar essa divergência. Uma mesma área pode ser reofertada e os processos não são identificadores invariáveis de terrenos físicos.

### Por que a 6ª e a 7ª ficaram fora do treinamento

A 6ª rodada emprega avaliação social: 171 áreas requeridas, 43 não requeridas, 204 livres e 2 retiradas. Seu desfecho não é comparável a um lance financeiro de proposta fechada. A 7ª está integralmente marcada como edital cancelado: 4.647 registros. Tratá-los como lances zero induziria um alvo errado. Ambas agora aparecem no painel e na base, com explicação própria.

## 5. Experimentos de aprendizado de máquina

### Alvos

1. Classificação: ocorrência de arrematação com lance positivo entre resultados comerciais válidos.
2. Regressão: valor do lance condicionado a uma arrematação, treinado em `log(1 + valor)`.
3. Quantis experimentais: faixas inferior e superior para os lances positivos; não são intervalos calibrados.

Não há modelo validado de recebimento. Para isso seriam necessários dados de vencimento, pagamento, parcelamento, desistência, sanções e conciliação. Uma previsão central em escala logarítmica não deve ser somada como valor esperado de receita.

### Variáveis e cortes

As variáveis básicas são UF, regime, área em hectares e ano do processo. As históricas incluem contagens de eventos por código, tempo desde o último evento, títulos publicados, substâncias com início anterior ao corte e número de titulares/requerentes históricos. Identidades individuais não são preditores.

Cortes conservadores: 01/01/2020 para rodadas 1–2; 01/01/2021 para 3–5; 01/01/2024 para 8. Eventos posteriores são excluídos das variáveis de treino, ainda que apareçam na ficha histórica. Datas de ocorrência não garantem que a informação estivesse publicamente disponível naquela data.

O contexto territorial usa CFEM e DIPEM municipais de três anos, terminando dois anos antes do corte, indicadores de ausência e associações anteriores. Vínculos territoriais são os atuais. A composição adicional de rodada considera tamanho da oferta, concentração por UF, proporção de regimes, área mediana, idade dos processos e IPCA conhecido até novembro anterior ao corte anual.

### Validação

Seleção: rodadas 1–3 para treino e 5 para validação. A rodada 4 foi excluída desse treino porque sua homologação ocorreu após a abertura da 5ª. Após escolher os modelos, refaz-se o treino nas rodadas 1–5 para avaliar a 8ª. Processos que reaparecem na avaliação são removidos do treino. A 8ª já havia sido examinada na versão inicial; portanto, não é um teste prospectivo intocado.

| Experimento na 8ª | AUC ↑ | Brier ↓ | RMSLE ↓ | MAE dos lances positivos (R$) ↓ |
|---|---:|---:|---:|---:|
| Referência constante | 0,500 | 0,381 | 2,143 | 168.348,93 |
| Floresta histórica inicial | 0,665 | 0,300 | 1,944 | 165.641,31 |
| V2 escolhida na 5ª | 0,657 | 0,314 | 1,944 | 165.611,37 |
| Contexto de rodada + inflação, diagnóstico retrospectivo | 0,707 | 0,255 | 1,822 | 162.858,75 |

A V2 selecionou boosting básico para ocorrência e floresta histórica para lance. O modelo ampliado melhorou a avaliação na 8ª, mas seu Brier piorou na validação da 5ª (0,215, contra 0,182 do candidato básico). Isso não sustenta substituição automática nem ganho uniforme. O experimento tem variáveis retrospectivas e não constitui prova de desempenho utilizável antes do edital.

A faixa de quantis 10%–90% cobriu 62,33% dos lances positivos na 8ª, abaixo dos 80% nominais. É necessário calibrar e reavaliar. A mediana da largura da faixa foi aproximadamente R$ 76,1 mil. Não se deve comunicar uma “precisão de 80%”.

## 6. O que mudou entre rodadas

A primeira rodada foi um piloto ligado sobretudo a minerais para infraestrutura e construção civil. A oferta seguinte ampliou substâncias e modalidades. Os dados mostram que a taxa de arrematação positiva no conjunto das rodadas 1–5 era cerca de 26,3%; na 8ª foi 65,9%. A mediana positiva passou de R$ 10,1 mil para R$ 31,6 mil. A composição por UF também mudou: distância de variação total aproximada de 15,6% entre distribuições.

O Relatório de Gestão 2024 da ANM registra 4.581 áreas nominadas entre 5.000 ofertadas (91,62%), indicando seleção com interesse de mercado. Registra também integração SOPLE–REPEM e substituição de GRU por boletos. São hipóteses explicativas relevantes, mas um percentual divulgado depois da rodada não deve ser usado como se fosse uma variável pública conhecida antes do leilão. É necessário recuperar a nominação histórica por área e sua data de publicação.

Há ainda um limite temporal decisivo: o próprio relatório informa abertura do SOPLE em setembro de 2024 e início da abertura da DIPEM em outubro de 2024. Os anos de referência da DIPEM podem ser anteriores, mas sua abertura ocorreu depois da 8ª rodada. Por isso, as faixas e modelos territoriais que a usam são diagnósticos retrospectivos. A fonte poderia ter utilidade prospectiva em rodadas posteriores, com versões preservadas.

Documentos preparatórios da 9ª propõem participação da B3, taxas, valor mínimo e garantias. Uma nota técnica menciona limite de interesse de 20%; notícia posterior menciona 10%. Essa divergência reforça a necessidade de vincular cada variável à versão final do edital. O painel não trata minutas como regras vigentes. Valores mínimos, prazos e garantias sem confirmação integral permanecem pendentes, em vez de receber números presumidos.

## 7. Atualização automática

A rotina diária verifica dez arquivos públicos da ANM, compara metadados e conteúdo, valida esquemas, número de linhas, arquivos ZIP e rodadas conhecidas. Quando há mudanças válidas, guarda a extração anterior, reconstrói as associações, geometrias, detalhes e base analítica, e prepara nova publicação. Uma rodada desconhecida ou mudança de esquema interrompe a atualização para revisão.

O navegador procura uma versão publicada a cada cinco minutos e permite consulta manual. As datas de extração e de modificação informadas pelos servidores são exibidas separadamente. Nenhum desses mecanismos significa acesso a lances sigilosos em andamento.

Os modelos e os relatórios científicos permanecem congelados. Quando as fontes relevantes mudam, a exibição de previsões é desativada até revisão documentada. A publicação automática depende da tarefa local, do Codex e do computador/rede disponíveis; não é uma infraestrutura independente de operação 24 horas.

## 8. Críticas e próxima etapa científica

- Muitos registros não equivalem a muitas experiências independentes: há somente seis rodadas comerciais utilizadas.
- Há seleção de áreas, mudança de regras, crescimento de interesse e defasagem econômica. Separação aleatória de linhas produziria confiança excessiva.
- Os anexos originais e suas retificações ainda precisam ser conciliados integralmente. As composições reconstruídas dos resultados atuais podem refletir retiradas posteriores.
- Históricos atuais podem ter correções retroativas. É necessário preservar versões e horários de disponibilidade, não apenas datas dos eventos.
- Não há aqui distribuição completa de lances perdedores, valores privados, custos ou riscos dos participantes. Não é possível inferir lance ótimo individual com confiança.
- O contexto municipal não prova potencial geológico da área. A geometria atual não prova ausência de restrições ou disponibilidade jurídica.
- Modelos lineares e árvores não identificam causalmente os efeitos de uma regra de edital. Uma intervenção inédita não tem efeito estimável apenas por adicionar uma variável binária constante nos leilões anteriores.
- É necessário avaliar calibração, erros por UF/substância, sensibilidade a valores extremos e desempenho em novas rodadas, com períodos futuros reservados.

Para o Prêmio Belmiro Siqueira 2026, o argumento mais defensável é a gestão integrada, auditável e explicável de decisões, com avaliação honesta de incerteza. O ganho gerencial deve ser medido em tempo de análise, capacidade de identificar inconsistências, rastreabilidade e utilidade para gestores. Não convém alegar pioneirismo absoluto: a ANM já descreve projetos DataVista e GeoPotencial.

## 9. Fontes e reprodução

- [Catálogo ANM](https://www.gov.br/anm/pt-br/acesso-a-informacao/dados-abertos/bases-de-dados)
- [SOPLE](https://dadosabertos.anm.gov.br/SOPLE/)
- [Cadastro Mineiro](https://dadosabertos.anm.gov.br/SCM/microdados/)
- [SIGMINE](https://dadosabertos.anm.gov.br/SIGMINE/PROCESSOS_MINERARIOS/)
- [CFEM](https://dadosabertos.anm.gov.br/CFEM/) e [DIPEM](https://dadosabertos.anm.gov.br/DIPEM/)
- [Relatório de Gestão ANM 2024](https://www.gov.br/anm/pt-br/acesso-a-informacao/acoes-e-programas/governanca/gestao-estrategica/relatorio-gestao/relatorio-de-gestao_2024_versao-para-apresentacao-1.pdf/@@download/file), especialmente páginas 20, 29–30 e 97–103.
- [Nota técnica preparatória da 9ª rodada](https://www.gov.br/anm/pt-br/acesso-a-informacao/participacao-social/audiencias-publicas/audiencia-publica-n-o-02-2025/nota-tecnica-sei-no-19692025-cedsod-anmdirc-sei-n-16923293.pdf)
- [Notícia da audiência da 9ª rodada](https://www.gov.br/anm/pt-br/assuntos/noticias/audiencia-publica-debate-regras-de-oferta-publica-e-leilao-de-areas-aptas-para-mineracao)
- [API de malhas do IBGE](https://servicodados.ibge.gov.br/api/docs/malhas?versao=3)
- [IPCA mensal, SGS 433](https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/01/2015&dataFinal=31/12/2023)
- [Logo fornecido](https://commons.wikimedia.org/wiki/File:LogoANM.jpg) e [gov.br Design System](https://www.gov.br/ds/)

Os arquivos JSON dos experimentos guardam métricas e limitações. O SQLite conserva tabelas relacionais e hashes de fontes; o pacote de código contém os scripts de integração, análise e atualização. Os scripts de treinamento pressupõem os arquivos de origem e as dependências Python indicadas. A versão congelada dos relatórios deve ser preservada ao atualizar o painel.


## Ampliação: todas as rodadas e estoque completo

A interface passa a se chamar **MinerIA — Inteligência para a Gestão de Leilões Minerais**. A visão geral começa pelos lances vencedores acumulados e organiza as rodadas da 1ª à 8ª. O acumulado é calculado em ordem cronológica e apresentado em ordem cronológica. Os valores são nominais e não comprovam pagamentos.

As oito rodadas permanecem visíveis: a 6ª possui avaliação social, a 7ª está cancelada e não recebe métricas financeiras iguais a zero. A exploração tem filtros específicos de processo (DSProcesso) e substância, além da busca livre, do estado, município e resultado. O DSProcesso usa seis dígitos antes da barra, completados com zeros à esquerda, e ano de quatro dígitos: `000.000/0000`.

O estoque contém **149.362 processos**: 64.507 para análise, 58.160 não aptos para disponibilidade, 18.296 aptos e 8.399 em análise. Esses status pertencem ao retrato atual; não reconstituem o estoque em cada ano. A ficha mostra uso da substância, regime, indicação de interesse, fase, situação do processo, situação do estoque, inclusão em edital e última situação em edital. Há vínculo com características do estoque para 23.549 dos 23.554 processos das rodadas; cinco não possuem esse vínculo.

O perfil compara todos os resultados de todas as rodadas, por estado, com mediana do tamanho, principais substâncias, regimes e usos. Um processo pode ter mais de uma substância e reaparecer em outra rodada. Diferenças de perfil são associações, não causas demonstradas. A condição Livre em uma rodada não prova que o processo está disponível hoje. Os eventos ajudam a investigar a entrada em disponibilidade, mas a causa deve ser confirmada no ato administrativo; não foi inventado um motivo único a partir do status.

O universo unido de estoque e rodadas contém 149,367 processos, 149,192 com poligonal e 2,629,419 eventos disponíveis. Lacunas são apresentadas como ausência, sem desenhar limites fictícios.

O treinamento permanece temporal e restrito às seis rodadas comerciais. A cobertura descritiva ampliada não significa que existe previsão validada para todo o estoque. Testes fora do treino publicados continuam restritos à 8ª rodada, com escolha de modelo realizada na 5ª. Essa distinção é indispensável para não apresentar ajuste ao passado como previsão do futuro.

## Siglas

- SOPLE: Sistema de Oferta Pública e Leilão de Áreas.
- SCM: Sistema de Cadastro Mineiro.
- SIGMINE: Sistema de Informações Geográficas da Mineração.
- CFEM: Compensação Financeira pela Exploração de Recursos Minerais, distinta de lances de leilão.
- DIPEM: Declaração de Investimento em Pesquisa Mineral.

A atualização foi agendada diariamente às 8h no aplicativo. Depende do computador e do aplicativo disponíveis. O navegador procura novas versões publicadas a cada cinco minutos; isso não corresponde a lances em tempo real. Revisões nas fontes preservam as extrações anteriores e desabilitam previsões antigas até revisão. Novas rodadas exigem conferir regras, fases e esquema antes de publicar.


## Revisão visual e leitura das rodadas especiais

O nome da interface passa a ser **MinerIA**, com IA em destaque e subtítulo “Inteligência para a gestão de leilões minerais”. O gráfico usa barras para o acréscimo de cada rodada e uma linha para o total acumulado, na mesma escala em reais. A apresentação mantém a ordem da 1ª à 8ª; o cálculo do acumulado permanece cronológico, da 1ª até cada rodada.

A 6ª rodada foi destinada à Permissão de Lavra Garimpeira e utilizou avaliação social para definir prioridade de requerimento, por critérios objetivos. Requerimento não equivale a título concedido. A notícia oficial de lançamento descreve a modalidade e critérios: https://www.gov.br/anm/pt-br/anm-lanca-sexta-rodada-de-oferta-publica-de-areas-para-mineracao

A 7ª rodada corresponde ao Edital nº 2/2022, cancelado pela Decisão nº 6530084/GAB-DG/ANM/2023, publicada em 22/02/2023 e referendada em 27/03/2023. A ata confirma o ato, sem detalhar a motivação técnica: https://www.gov.br/anm/pt-br/acesso-a-informacao/institucional/reunioes-da-diretoria-colegiada/ata-49a-reuniao-ordinaria-publica-diretoria-colegiada.pdf

Nos dois casos, a marca 0* no gráfico significa acréscimo nulo ao acumulado de lances comparáveis; não significa arrematação por R$ 0. A linha mantém o total da 5ª rodada. As fichas e métricas comerciais continuam indicando “não se aplica”. A tabela acessível sob o gráfico permite conferir os valores.

O botão Tela cheia permite expandir o painel, com saída pelo mesmo botão ou Esc. Quando o navegador não autoriza tela cheia, o painel oferece modo ampliado dentro da janela e informa essa limitação. A tipografia utiliza Rawline da distribuição oficial e os tokens do Design System gov.br 3.7.0, com texto de 16,8 px, controles de 14 px e títulos na escala oficial.
