from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from dataclasses import dataclass
import time
import csv

@dataclass
class Carro:
    modelo: str
    valor: str
    ano: str
    km: str
    historico: str
    local: str

def extrair_dados(driver):
    """Coleta os dados dos carros na página atual."""
    registros = []
    itens = driver.find_elements(By.CSS_SELECTOR, ".ui-search-layout__item")

    for item in itens:
        try:
            modelo = item.find_element(By.CSS_SELECTOR, ".poly-component__title-wrapper a").text
            valor = item.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction").text
            atributos = item.find_elements(By.CSS_SELECTOR, ".poly-attributes-list__item")

            ano = atributos[0].text if len(atributos) > 0 else "N/A"
            km = atributos[1].text if len(atributos) > 1 else "N/A"

            historico = item.find_element(By.CSS_SELECTOR, ".poly-component__visit-history").text
            local = item.find_element(By.CSS_SELECTOR, ".poly-component__location").text

            registro = Carro(modelo, valor, ano, km, historico, local)
            registros.append(registro)

        except Exception as e:
            print(f"Erro ao processar item: {e}")
    
    return registros

def proxima_pagina(driver):
    """Verifica se há próxima página e avança para ela."""
    try:
        # Aguarda o botão "Seguinte" estar visível
        proximo = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Seguinte"]'))
        )
        
        # Usando JavaScript para clicar no botão "Seguinte", ignorando qualquer obstrução visual
        driver.execute_script("arguments[0].click();", proximo)
        
        time.sleep(5)  # Aguarda o carregamento da página
        return True  # Indica que avançou
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print(f"Erro ao tentar avançar para a próxima página: {e}")
        return False  # Indica que não há mais páginas ou houve erro

def raspar_paginas(driver):
    """Executa a raspagem de todas as páginas disponíveis."""
    registros = []
    
    while True:
        registros.extend(extrair_dados(driver))  # Extrai dados da página atual
        if not proxima_pagina(driver):  # Se não houver próxima página, encerra
            break

    return registros

def salvar_em_csv(dados, nome_arquivo):
    """Salva os dados extraídos em um arquivo CSV."""
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Modelo", "Valor", "Ano", "KM", "Histórico", "Local"])  # Cabeçalho
        for carro in dados:
            writer.writerow([carro.modelo, carro.valor, carro.ano, carro.km, carro.historico, carro.local])

# Iniciar o navegador
driver = webdriver.Chrome()
driver.get("https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/_VEHICLE*BODY*TYPE_452759")

# Iniciar a raspagem
dados_extraidos = raspar_paginas(driver)

# Salvar os resultados em um arquivo CSV
salvar_em_csv(dados_extraidos, 'carros_extraidos.csv')

# Exibir os resultados
print(f"Total de carros extraídos: {len(dados_extraidos)}")
for carro in dados_extraidos:
    print(carro)

# Fechar o navegador
driver.quit()
