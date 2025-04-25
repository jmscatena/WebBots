"""
Esse exemplo cobre:
    • Download de páginas
    • Extração de dados (títulos)
    • Descoberta e enfileiramento de novos links para visitar[6][4][2]
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class FirstCrawler:
    def __init__(self, start_url):
        self.visited = set() # Inicializa variavel com um conjunto vazio de dados
        self.to_visit = [start_url] # Adiciona a URL a variavel to_visit

    def extract_and_print_data(self, soup, base_url):
        # Exemplo: extrair todos os títulos h1 da página
        for h1 in soup.find_all('h1'):
            print(f'Título encontrado: {h1.get_text(strip=True)}')

    def enqueue_links(self, soup, base_url):
        # Procura por Links (a) no html e adiciona a variavel to_visit caso nao tenha visitado ainda
        for link in soup.find_all('a', href=True):
            abs_url = urljoin(base_url, link['href'])
            if abs_url not in self.visited and abs_url not in self.to_visit:
                self.to_visit.append(abs_url)

    def crawl(self): # Codigo que visita todos os links da pagina
        while self.to_visit:
            url = self.to_visit.pop(0) #Remove o primeiro link da lista para visitar
            if url in self.visited:
                continue
            print(f'Crawling: {url}')
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser') # Captura o html e separa por tag
                    self.extract_and_print_data(soup, url) #Imprime os titulos H1
                    self.enqueue_links(soup, url) # Procura por Links - Ancoras <a> no html
                else:
                    print(f'Failed to retrieve {url}')
            except Exception as e:
                print(f'Error crawling {url}: {e}')
            self.visited.add(url) # Se tudo der certo adiciona a variavel visited


if __name__ == '__main__':
    start_url = 'https://www.uol.com.br'
    crawler = FirstCrawler(start_url)
    crawler.crawl()
