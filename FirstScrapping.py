"""
    Emojis retirados do site : emojipedia.org

"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


class FirstScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        self.produtos = []

        print("🚀 Navegador Chrome inicializado em modo headless")

    def fazer_pesquisa(self, termo):
        print(f"\n🔍 Pesquisando por '{termo}'...")
        self.driver.get("https://www.scrapingcourse.com/ecommerce")
        # Realiza a busca pelo componente do tipo input search
        search_box = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
        )
        search_box.send_keys(termo) # Adicionao conteudo ao campo
        search_box.submit() # Envia o formulario
        print("✅ Pesquisa concluída com sucesso")

    def coletar_links_produtos(self):
        print("\n📦 Coletando links dos produtos...")
        elements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product a"))
        )
        # Contabiliza a quantidade de produtos
        links = [element.get_attribute("href") for element in elements]
        print(f"✅ {len(links)} produtos encontrados")
        return links

    def extrair_dados_produto(self, url):
        try:
            self.driver.get(url)
            print(f"\n👉 Acessando produto: {url}")
            produto = {
                "titulo": self.wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.product_title"))
                ).text,
                "conteudo": self.wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "div.woocommerce-product-details__short-description"))
                ).text
            }
            print("✅ Dados extraídos com sucesso")
            return produto
        except Exception as e:
            print(f"❌ Erro ao processar {url}: {str(e)}")
            return None

    def salvar_json(self, filename):
        print(f"\n")
        print(f"\n💾 Salvando resultados em {filename}...")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.produtos, f, ensure_ascii=False, indent=4)
        print("✅ Arquivo salvo com sucesso ")

    def executar_scraping(self, termo_pesquisa):
        try:
            self.fazer_pesquisa(termo_pesquisa)
            links = self.coletar_links_produtos()

            for link in links:
                dados = self.extrair_dados_produto(link)
                if dados:
                    self.produtos.append(dados)
                time.sleep(1)

            self.salvar_json('produtos.json')
        finally:
            self.driver.quit()
            print("\n🛑 Navegador finalizado 🔥")


if __name__ == "__main__":
    scraper = FirstScraper()
    scraper.executar_scraping("tshirt")
