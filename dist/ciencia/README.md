# LanceMineral IA — ciência aberta e reprodução

Versão de pesquisa, extração de 24/09/2026. Este pacote permite conferir os insumos, reconstruir os dois modelos selecionados e comparar as métricas obtidas com as publicadas. Não há recomendação de lance nem previsão validada de receita recebida.

## Resposta direta: o modelo é bom?

**Útil como experimento e referência para pesquisa, ainda insuficiente como ferramenta autônoma de decisão financeira.** A classificação discrimina moderadamente os casos, a precisão monetária é limitada e os intervalos estão subcalibrados. O valor demonstrado do projeto neste estágio é integrar, auditar e explorar os dados, além de oferecer um protocolo preditivo verificável. Não está demonstrada economia de recursos, incremento de receita ou superioridade operacional sobre especialistas.

Veja a ficha detalhada em `FICHA_DO_MODELO.md`.

## Reproduzir com Python

O ambiente utilizado foi Python 3.12.14. As versões exatas estão em `ambiente.json` e `requirements.txt`. Use um ambiente virtual separado. Não é necessário executar o painel.

```shell
python -m venv .venv
```

Ativação no Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Ativação no Linux/macOS:

```shell
source .venv/bin/activate
```

Depois, em qualquer sistema:

```shell
python -m pip install -r requirements.txt
python reproduzir.py --verificar
python reproduzir.py --selecionados
python reproduzir.py --completo
```

- `--verificar`: confere o hash SHA-256, a unicidade das observações, os alvos, os cortes e a separação dos processos entre treino e teste. Não treina.
- `--selecionados`: reconstrói os dois modelos escolhidos no experimento V2, prevê a 8ª rodada e compara quatro métricas com o relatório original.
- `--completo`: também repete os seis candidatos na 5ª rodada, a escolha dos modelos e as faixas de quantis. O diagnóstico adicional de contexto entre rodadas está no código original `round_changes.py`; não é executado por esta opção.

A execução salva `reproducao_resultado.json`, sem sobrescrever os relatórios de referência. Diferenças acima da tolerância numérica de uma parte por milhão interrompem a verificação. O tempo e a memória dependem do computador; o conjunto histórico usa matrizes densas. Recomenda-se alguns GB livres de memória. Não foram realizados testes de portabilidade em todos os sistemas ou versões alternativas.

## O que está no pacote

| Arquivo/pasta | Função |
|---|---|
| `reproduzir.py` | Implementação legível e independente para reprodução do experimento V2 |
| `dados/experimento_congelado.json.gz` | 21.175 observações e conjuntos de variáveis efetivamente utilizados |
| `manifesto.json` | Esquema, contagens e SHA-256 do insumo congelado |
| `resultados_referencia/` | Resultados originais, auditorias e contagens da integração |
| `codigo_original/` | Scripts originais de integração, treinamento, comparação e atualização |
| `FICHA_DO_MODELO.md` | Objetivo, variáveis, protocolo, resultados e limitações |
| `variaveis_expandidas.csv` | Todas as colunas codificadas efetivamente aprendidas no treino final |
| `requirements.txt`, `ambiente.json` | Dependências fixadas e ambiente utilizado |
| `FONTES.md` | Origens dos dados e distinção entre fotografia congelada e fonte atual |

Não são incluídos nomes de participantes, CPF/CNPJ, identificadores de titulares nem textos livres administrativos. O atributo de titulares contém apenas uma contagem histórica. O código de reprodução usa JSON comprimido, não exige abrir arquivos Python serializados com pickle.

## Como conferir a integração desde os arquivos da ANM

Os scripts originais preservam a organização `work/`, `outputs/` e `painel-anm/dist/` do projeto. Para reconstruir desde a origem: baixe as fontes descritas em `FONTES.md` para `work/`, coloque os scripts originais nesse diretório, instale também `pyshp==3.1.6` para as poligonais e execute, nesta ordem:

1. `integrate_scm.py`: relaciona os processos de estoque/rodadas aos microdados cadastrais.
2. `experiment_ml.py`: constrói as variáveis, treina as referências e o estudo inicial.
3. `experiment_v2.py`: repete a seleção temporal e a avaliação dos modelos V2.
4. `round_changes.py`: diagnóstico adicional; requer também a série IPCA em `work/ipca.json`.

Os scripts de mapa e painel constituem outra etapa: `geo_extract.py`, `build_details.py`, `prepare_context.py`, `build_dashboard_data.py`, `build_overview.py`, `build_stock.py` e `build_database.py`. Eles exigem a árvore do projeto e os arquivos indicados no código. A rotina `update_pipeline.py` é operacional e modifica o retrato local; **não** deve ser usada para reproduzir a fotografia congelada.

Baixar os arquivos atuais da ANM pode gerar resultados diferentes porque as fontes são revisadas. A reprodução exata das métricas é assegurada pelo insumo congelado do pacote; a reconstrução independente desde os arquivos brutos da mesma data exige preservar também essas extrações. Este ZIP não inclui todos os arquivos brutos, que somam centenas de MB. O pacote SQLite da entrega contém a integração local, e os hashes de origem estão no seu inventário.

## Publicação científica e limites de abertura

O código e os dados derivados são disponibilizados para inspeção e reprodução neste protótipo. Ainda não há repositório público versionado, DOI, licença de reutilização formalizada nem registro prévio do protocolo. Portanto, esta entrega **não deve ser descrita como um repositório científico público arquivado**. Para o artigo: atribuir autoria, escolher uma licença compatível com as fontes, publicar uma versão numerada em repositório público e arquivá-la com identificador permanente, incluindo este manifesto e a referência da versão usada. O Site continua com acesso privado.

Não há nomes de autores no material experimental para que a versão destinada à avaliação do prêmio possa ser preparada conforme as regras de anonimização; isso não substitui a revisão final do artigo e do edital.

## Verificação realizada nesta entrega

A execução `--completo` foi concluída no ambiente registrado. Os seis candidatos, a escolha dos modelos, as quatro métricas da 8ª rodada e a cobertura de 62,3313% foram reproduzidos. Houve diferenças apenas de arredondamento numérico, dentro da tolerância de uma parte por milhão. O resultado integral está em `reproducao_resultado.json`. Isso comprova reprodução computacional local; não substitui validação futura ou revisão independente.

A interface atual se chama **MinerIA**. Os nomes LanceMineral/GeoLance em arquivos históricos identificam versões anteriores do mesmo experimento. A revisão visual não altera os dados ou as métricas congeladas.
