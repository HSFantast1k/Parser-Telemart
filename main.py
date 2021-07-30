import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
base_list = []

def parser_of_goods(link_product):
    response = requests.get(link_product, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    base_list.append([
        'Название - {}'.format(soup.find('h1', 'b-page-title').get_text()),
        'Цена - {}'.format(soup.find('div', class_='b-price').get_text()),
        'Наличие - {}'.format('None')
    ])
    if soup.find('div', 'b-i-product-available b-i-product-available-green').get_text() == 'Есть в наличии':
        base_list[-1][-1] = 'Наличие {}'.format(True)
    else:
        base_list[-1][-1] = 'Наличие {}'.format(False)
    print(base_list)

def parser_page():
    page = 1
    while True:
        if page == 1:
            response = requests.get('https://telemart.ua/laptops/', headers=HEADERS)
        else:
            response = requests.get('https://telemart.ua/laptops/p{}/'.format(page), headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='b-i-product-inner')
        if len(items):
            print(page)
            for item in items:
                print(item.find('div', 'b-i-product-name').find('a').get('href'))
                parser_of_goods(item.find('div', 'b-i-product-name').find('a').get('href'))
            page += 1
        else:
            return

parser_page()
