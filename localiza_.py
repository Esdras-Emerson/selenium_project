from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from dataclasses import dataclass
import csv
import time

@dataclass
class Carro:
    marca: str
    modelo: str
    valor: str
    ano: str
    km: str
    transm: str
    local: str

def extrair_valor(item, selectors, timeout=10):
    """
    Aguarda até que algum dos seletores fornecidos retorne um texto não vazio.
    Se nenhum for encontrado dentro do timeout, retorna "Não informado".
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        for selector in selectors:
            try:
                valor = item.find_element(By.CSS_SELECTOR, selector).text.strip()
                if valor:
                    return valor
            except NoSuchElementException:
                continue
        time.sleep(0.5)
    return "Não informado"

def extrair_dados(driver):
    """Extrai os dados dos carros carregados (elementos 'app-card-vehicle')."""
    registros = []
    itens = driver.find_elements(By.CSS_SELECTOR, "app-card-vehicle")
    for item in itens:
        try:
            marca = item.find_element(By.CSS_SELECTOR, ".title-car").text.strip()
            modelo = item.find_element(By.CSS_SELECTOR, ".subtitle-car-primary.ng-star-inserted").text.strip()
            
            # Usa a função auxiliar para extrair o valor aguardando que ele seja carregado
            valor = extrair_valor(item, [".text-price.yea-offers", ".text-price-of", ".price-tag-fraction"])
            
            # Para ano e km, removemos separadores indesejados
            ano = item.find_element(By.CSS_SELECTOR, ".text-km").text.strip().split("|")[0].strip()
            km = item.find_element(By.CSS_SELECTOR, ".text-milage").text.strip().split("|")[0].strip()
            try:
                transm = item.find_element(By.CSS_SELECTOR, ".text-gearbox.ng-star-inserted").text.strip()
            except NoSuchElementException:
                transm = "Não informado"
            try:
                local = item.find_element(By.CSS_SELECTOR, ".text-location").text.strip()
            except NoSuchElementException:
                local = "Não informado"
            registro = Carro(marca, modelo, valor, ano, km, transm, local)
            registros.append(registro)
        except NoSuchElementException as e:
            print(f"Erro ao processar item: {e}")
    return registros

def salvar_em_csv(dados, nome_arquivo):
    """Salva os dados extraídos em um arquivo CSV."""
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Marca", "Modelo", "Valor", "Ano", "KM", "Transm", "Local"])
        for carro in dados:
            writer.writerow([carro.marca, carro.modelo, carro.valor, carro.ano, carro.km, carro.transm, carro.local])

def clicar_mostrar_mais(driver):
    """Clica no botão 'Mostrar mais', aguardando que o overlay seja removido."""
    try:
        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "ins-frameless-overlay"))
            )
        except TimeoutException:
            driver.execute_script("document.getElementById('ins-frameless-overlay').style.display='none';")
            print("Overlay removido via JavaScript.")
        botao = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn-show-more-plp-2"))
        )
        botao.click()
        time.sleep(2)
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print("Erro ao clicar no botão 'Mostrar mais':", e)

def scroll_infinite(driver, delay=1, timeout=30):
    """
    Realiza scroll infinito até que não sejam carregados novos itens por 'timeout' segundos.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    start_time = time.time()
    registros = []

    while True:
        # Realiza a raspagem de dados antes de rolar para baixo
        novos_registros = extrair_dados(driver)
        registros.extend(novos_registros)
        print(f"Total de carros extraídos até agora: {len(registros)}")

        # Rola para baixo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height > last_height:
            last_height = new_height
            start_time = time.time()
        else:
            if time.time() - start_time > timeout:
                break

    print("Scroll infinito finalizado. Altura final da página:", last_height)
    return registros

# Inicia o navegador e carrega a página
driver = webdriver.Chrome()
driver.get("https://seminovos.localiza.com/carros/rj-rio-de-janeiro?cidade=rj-rio-de-janeiro")
time.sleep(3)

# Extrai os 14 carros iniciais
dados_iniciais = extrair_dados(driver)
print(f"Carros iniciais carregados: {len(dados_iniciais)}")

# Clica uma única vez no botão "Mostrar mais"
clicar_mostrar_mais(driver)

# Realiza scroll infinito para carregar os demais itens
dados_finais = scroll_infinite(driver, delay=1, timeout=30)
# Aguarda um pouco extra para que os dados se estabilizem
time.sleep(5)

# Salva os dados extraídos em um arquivo CSV
salvar_em_csv(dados_finais, 'carros_extraidos.csv')

# Exibe os primeiros 5 carros extraídos
for carro in dados_finais[:5]:
    print(carro)

# Fecha o navegador
driver.quit()
