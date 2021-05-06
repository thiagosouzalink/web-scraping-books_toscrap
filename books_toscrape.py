import requests
from bs4 import BeautifulSoup
import pandas as pd

# Link de acesso
url = "https://books.toscrape.com/"
page_catalogue = "https://books.toscrape.com/catalogue/page-"

# Recebe conteudo da página
response = requests.get(url)
response_page = BeautifulSoup(response.text, 'html.parser')

# Obtem o tal de páginas
text_num_pages = response_page.find('li', {'class': 'current'}).text.strip()
total_pages = int(text_num_pages.split()[3])

catalogo_livros = [] # Lista para obter todos os livros

# Percorrer todas as páginas
for num_page in range(1, total_pages+1):
    # Acesso as páginas
    pagina = f"{page_catalogue}{num_page}.html"
    response = requests.get(pagina)
    # Recebe boxes dos livros
    response_page = BeautifulSoup(response.text, 'html.parser')
    livros = response_page.find_all('article', {'class': 'product_pod'})

    # Percorre pelos boxes dos livros
    for livro in livros:
        # Obtem titulo, preço e link de cada livro
        titulo = livro.find('h3').a['title']
        preco = float(livro.find('p', {'class': 'price_color'}).text.lstrip('Â£'))
        ancora = livro.find('a')['href']
        link = f"{url}{ancora}"
        catalogo_livros.append(dict(titulo=titulo, preco=preco, link=link))
    

# Carrega Dataframe contendo os livros
df = pd.DataFrame(data=catalogo_livros)
df.columns = ['Título', 'Preço', 'Link']
# Ordena o dataframe pelo preço
df = df.sort_values(by=['Preço'], ascending=False)

# Salva o dataframe como arquivo xlsx
df.to_excel('catalogo_livros.xlsx', index=False)