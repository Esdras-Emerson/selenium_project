# Selenium Project

Este projeto utiliza a biblioteca Selenium para realizar a raspagem de dados (web scraping) de sites de venda de veículos e outras fontes de dados. O objetivo é extrair informações detalhadas sobre os carros listados e outros dados relevantes, e salvar esses dados em um arquivo CSV para análise posterior.

## Estrutura do Projeto

### Arquivos Principais

- `carro_ml2.py`: Este script realiza a raspagem de dados do site Mercado Livre, especificamente da seção de veículos. Ele navega pelas páginas de listagem de carros, extrai informações detalhadas de cada carro e salva os dados em um arquivo CSV.

- `localiza_.py`: Este script realiza a raspagem de dados do site Localiza Seminovos. Ele utiliza uma técnica de scroll infinito para carregar todos os carros listados na página, extrai informações detalhadas de cada carro e salva os dados em um arquivo CSV.

- `tabelas_site.py`: Este script realiza a raspagem de dados de tabelas HTML de uma página da Wikipedia. Ele navega até a página especificada, lê as tabelas HTML e imprime o número de tabelas encontradas.

### Funções Principais

#### `carro_ml2.py`

- `extrair_dados(driver)`: Extrai os dados dos carros carregados na página atual.
- `salvar_em_csv(dados, nome_arquivo)`: Salva os dados extraídos em um arquivo CSV.
- `scroll_infinite(driver, delay, timeout)`: Realiza scroll infinito até que não sejam carregados novos itens por um determinado tempo.

#### `localiza_.py`

- `extrair_valor(item, selectors, timeout, retries)`: Aguarda até que algum dos seletores fornecidos retorne um texto não vazio. Se nenhum for encontrado dentro do timeout, retorna "Não informado".
- `extrair_dados(driver)`: Extrai os dados dos carros carregados na página atual.
- `salvar_em_csv(dados, nome_arquivo)`: Salva os dados extraídos em um arquivo CSV.
- `clicar_mostrar_mais(driver)`: Clica no botão "Mostrar mais", aguardando que o overlay seja removido.
- `scroll_infinite(driver, delay, timeout)`: Realiza scroll infinito até que não sejam carregados novos itens por um determinado tempo.

#### `tabelas_site.py`

- `driver.get(url)`: Navega até a página da Wikipedia especificada.
- `pd.read_html(StringIO(driver.page_source))`: Lê as tabelas HTML da página e retorna uma lista de DataFrames.
- `print(f"Number of tables found: {len(tables)}")`: Imprime o número de tabelas encontradas na página.

## Como Executar
1. Clone o repositório para o seu ambiente local:

```bash
git clone <URL_DO_REPOSITORIO>
cd selenium_project

2. Certifique-se de ter o Python e o Selenium instalados em seu ambiente.
3. Baixe o driver do navegador correspondente (por exemplo, ChromeDriver para Google Chrome) e adicione-o ao PATH do sistema.
4. Utilize o Uv para criar e ativar um ambiente virtual:

```bash
uv new selenium_project_env
uv activate selenium_project_env