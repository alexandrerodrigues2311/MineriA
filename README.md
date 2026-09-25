# MineriA

Inteligência para leilões minerais. Painel estático com dados abertos, avaliações retrospectivas de aprendizado de máquina e exploração de áreas.

## Executar localmente

Na raiz deste diretório: `python -m http.server 8774 --directory dist`.
Acesse http://localhost:8774. Não é necessária instalação de pacotes para servir o painel.

## Publicação preparada

Nome solicitado do repositório: **MineriA**. Nome técnico sugerido do projeto Vercel: **mineria** (sujeito à disponibilidade na conta).
Importar este repositório na Vercel, com raiz neste diretório, preset Other e saída dist. vercel.json inclui as rotas /utilidade e /acervo. Não requer variáveis secretas para a versão estática.

Documentação da configuração: https://vercel.com/docs/project-configuration/vercel-json

Esta preparação local não comprova criação do repositório ou implantação na Vercel. As contas precisam estar conectadas antes da publicação.

## Dados, modelos e limitações

Coleta preservada: 24/09/2026. CFEM acompanhada até 2025. Não há conexão em tempo real. SOPLE, Cadastro Mineiro, CFEM e SIGMINE têm coberturas distintas; consulte Fontes e método no painel.
O teste histórico não constitui seleção automática para uma nova rodada. Lance não equivale a receita recebida. Produto de pesquisa, não serviço oficial da ANM.

Código científico e protocolos reproduzíveis: dist/pesquisa/mineria-ciencia-aberta-v5.zip e relatórios nessa pasta. A identidade visual e componentes de terceiros conservam suas próprias condições de uso.

## Escopo do repositório

Publicar somente este diretório do painel. Não incluir a pasta irmã work, extrações brutas, documentos de trabalho ou credenciais. Preservar a configuração .openai/hosting.json do endereço anterior; ela não configura a Vercel. Os arquivos JSON.gz são transporte sem perdas e os JSON originais são a alternativa de compatibilidade.
