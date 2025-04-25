"""
Passo a Passo do Desafio
1. Identificar o Token CSRF
    ◦ O formulário de login contém um campo oculto _token que deve ser incluído na requisição POST.
    ◦ Use BeautifulSoup para extrair o valor desse campo do HTML da página de login
2. Configurar a Sessão
    ◦ Utilize requests.Session() para manter cookies e headers entre requisições, essencial para persistir a autenticação[8].
3. Enviar Credenciais com o Token
    ◦ Monte um payload contendo email, senha (fornecidos pelo site) e o token CSRF extraído
"""

import requests
from bs4 import BeautifulSoup

# Configurar sessão e URLs
login_url = "https://www.scrapingcourse.com/login/csrf"
session = requests.Session()

# 1. Obter página de login e extrair CSRF
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")
csrf_token = soup.find("input", {"name": "_token"})["value"]  # Extrai o token

# 2. Preparar payload com credenciais
payload = {
    "_token": csrf_token,
    "email": "admin@example.com",  # Credenciais fornecidas pelo site
    "password": "password"
}

# 3. Enviar requisição POST para login
login_response = session.post(login_url, data=payload)

# Verificar sucesso (status 200 + conteúdo esperado)
if login_response.status_code == 200 and "product-item" in login_response.text:
    print("Login bem-sucedido! Dados dos produtos:")

    # Extrair dados da página protegida
    soup = BeautifulSoup(login_response.text, "html.parser")
    products = soup.find_all(class_="product-item")

    for product in products:
        name = product.find(class_="product-name").text.strip()
        price = product.find(class_="product-price").text.strip()
        print(f"- {name}: {price}")
else:
    print(f"Falha no login. Status: {login_response.status_code}")
