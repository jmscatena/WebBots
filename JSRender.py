from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do Chrome em modo headless (sem abrir janela)
options = Options()
options.add_argument("--headless=new")  # modo headless moderno
service = Service()  # gerencia o driver automaticamente (requer chromedriver no PATH)

# Inicializa o driver do Chrome
driver = webdriver.Chrome(service=service, options=options)

try:
    # Abre a página do desafio
    driver.get("https://www.scrapingcourse.com/javascript-rendering")

    # Espera até que os produtos estejam carregados no DOM
    #WebDriverWait(driver, 10).until(
    #    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#product-grid .product-item"))
    #)

    # Extrai os elementos dos produtos
    products_elements = driver.find_elements(By.CSS_SELECTOR, "#product-grid .product-item")

    products = []
    for item in products_elements:
        name = item.find_element(By.CSS_SELECTOR, ".product-name").text.strip()
        price = item.find_element(By.CSS_SELECTOR, ".product-price").text.strip()
        image_url = item.find_element(By.CSS_SELECTOR, ".product-image").get_attribute("src")
        products.append({
            "name": name,
            "price": price,
            "image_url": image_url
        })

    # Exibe os produtos extraídos
    for product in products:
        print(f"{product['name']} - {product['price']} - {product['image_url']}")

finally:
    driver.quit()