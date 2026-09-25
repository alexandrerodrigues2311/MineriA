# Padronização de substâncias — versão 1

Em 25/09/2026 foi introduzido um vocabulário de apresentação para evitar que duas grafias do mesmo conceito solicitado fragmentem filtros e contagens.

| Nomes de entrada | Nome exibido |
|---|---|
| Ouro; minério de ouro | Ouro |
| Ferro; minério de ferro | Minério de ferro |

A comparação ignora caixa, acentos e espaços repetidos. A lista de uma área é separada por ponto e vírgula ou barra cercada de espaços. Repetições do mesmo nome após a conversão são removidas dentro da mesma lista: ouro + minério de ouro passam a uma única menção a Ouro. Não são removidos processos ou ocorrências de rodadas.

A regra é explícita: não removemos genericamente o prefixo minério de de outras substâncias. Hematita, ouro nativo, ligas e outros nomes não são fundidos automaticamente, pois exigem validação semântica própria. A nomenclatura de apresentação não substitui a classificação mineralógica da ANM.

A transformação acontece ao carregar os dados no painel, inclusive tabelas, filtros, perfis, carteira apta e textos dos simuladores. Os arquivos JSON originais e os pacotes de ciência aberta permanecem intactos; nos objetos de consulta o valor original é preservado em campo com sufixo _original (posição 13 nas linhas matriciais do estoque). Downloads diretos dos JSON e pacotes científicos mantêm os nomes da fonte. As exportações de tabelas usam os nomes exibidos.

Nenhum modelo foi retreinado, nenhuma pontuação foi alterada e não houve revisão da lista estratégica de referência. Área, processo, resultado, valor do lance e CFEM não mudaram. Esta revisão não cria informação geológica.

O arquivo padronizacao_substancias.json registra regras e quantidades de menções originais por base. Menções de substância não equivalem a número de áreas únicas; uma mesma área pode ter vários nomes e aparecer em rodadas diferentes.
