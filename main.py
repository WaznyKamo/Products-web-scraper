from bs4 import BeautifulSoup
import requests
import csv
import random


def find_products_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    products_list_html = soup.find('ul', attrs={"class": "products-list"})
    links_with_text = ['http:' + a['href'] for a in soup.find_all('a', attrs={"class": "products-list__link"}, href=True) if a.text]    # pobranie wszystkich adresów i edycja ich do czytalnej formy
    return links_with_text


def import_data(urls_list, category, prod_id):
    for url in urls_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='html.parser')
        photo_html = soup.find('div', attrs={"class": "product-image-gallery__main-item"})
        photo_src = 'https:' + photo_html.find('img')['src']

        if soup.find('div', attrs={"class": "e-product-price__special"}):                                                               # jeśli produkt nie posiada ceny przecenionej, to brana jest bez przeceny
            price = soup.find('div', attrs={"class": "e-product-price__special"}).text[:-3].replace('\n', '').replace('"', '')
        elif soup.find('div', attrs={"class": "e-product-price__normal"}):
            price = soup.find('div', attrs={"class": "e-product-price__normal"}).text[:-3].replace('\n', '').replace('"', '')
        else:
            price = '450'
        name_list = soup.find('div', attrs={"class": "e-product-name"}).text.split('\n')                                                # pobranie całego bloku tekstu i wydzielenie z niego nazwy i modelu przedmiotu
        name = name_list[1]
        model = name_list[3]
        brand = soup.find('span', attrs={"class": "e-product-details-list__desc"}).text.replace('\n', '')
        description = soup.find('div', attrs={"class": "e-product-description__content"}).text.replace('\n', '').replace('"', '')
        sizes = soup.select('td.size-table__cell.size-table__cell--bold')                                                   # pobranie rozmiarów i zapisanie ich do innego pliku
        for size in sizes:
            sizes_writer.writerow([prod_id, 'Rozmiar:rozmiar:0', size.text.replace('\n', ''), random.randint(0, 100)])
        product_data = [prod_id, name, brand, model, category, description, price, photo_src]
        products_writer.writerow(product_data)
        prod_id = prod_id + 1
    return prod_id


product_id = 1

polbuty_meskie_urls = find_products_urls('https://www.eobuwie.com.pl/meskie/polbuty.html')
sportowe_meskie_urls = find_products_urls('https://www.eobuwie.com.pl/meskie/sportowe.html')
lacze_meskie_urls = find_products_urls('https://www.eobuwie.com.pl/meskie/klapki-i-sandaly.html')
polbuty_damskie_urls = find_products_urls('https://www.eobuwie.com.pl/damskie/polbuty.html')
sportowe_damskie_urls = find_products_urls('https://www.eobuwie.com.pl/damskie/sportowe.html')
lacze_damskie_urls = find_products_urls('https://www.eobuwie.com.pl/damskie/klapki-i-sandaly.html')

products_list = []
products_file = open('products.csv', 'w', newline='', encoding='utf-8')
products_writer = csv.writer(products_file, delimiter=';')
sizes_file = open('sizes.csv', 'w', newline='', encoding='utf-8')
sizes_writer = csv.writer(sizes_file, delimiter=';')

products_writer.writerow(['ID', 'Nazwa', 'Marka', 'Model', 'Kategoria', 'Opis', 'Cena', 'URL_zdjecia'])
sizes_writer.writerow(['Product ID', 'Attribute (Name:Position)', 'Value', 'Quantity'])


product_id = import_data(polbuty_meskie_urls, 'Męskie@Półbuty', product_id)
product_id = import_data(sportowe_meskie_urls, 'Męskie@Sportowe', product_id)
product_id = import_data(lacze_meskie_urls, 'Męskie@Klapki', product_id)
product_id = import_data(polbuty_damskie_urls, 'Damskie@Półbuty', product_id)
product_id = import_data(sportowe_damskie_urls, 'Damskie@Sportowe', product_id)
product_id = import_data(lacze_damskie_urls, 'Damskie@Klapki', product_id)


products_file.close()
sizes_file.close()
