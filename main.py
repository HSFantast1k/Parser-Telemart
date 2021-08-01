import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
base_list = []

def parser_of_goods(link_product): #Парсинг товара
    response = requests.get(link_product, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    print('Название: {}'.format(soup.find('h1', 'b-page-title').get_text()))
    base_list.append([
        'Название: {}'.format(soup.find('h1', 'b-page-title').get_text()),
        '{}'.format(soup.find('div', 'b-product-db-meta-top clearfix').find('div', class_='b-i-product-articul').get_text()),
        f'Силка на товар: {link_product}',
        'Цена: {}'.format(None),
        'Наличие: {}'.format(None)
    ])
    try:
        soup.find('div', 'b-i-product-available b-i-product-available-green').get_text()
        base_list[-1][-1] = 'Наличие: {}'.format(True)
        base_list[-1][-2] = 'Цена: {}'.format(
        soup.find('div', class_='b-pmi-col-left').find('div', class_="b-price").get_text())
    except:
        base_list[-1][-1] = 'Наличие: {}'.format(False)
        base_list[-1][-2] = 'Цена: {}'.format(None)

def parser_categories():
    list_catalog = ['https://telemart.ua/desktop-pc/', 'https://telemart.ua/noutbuki/',
                    'https://telemart.ua/komplektujuschie/', 'https://telemart.ua/periphery/',
                    'https://telemart.ua/wireless/', 'https://telemart.ua/monitors/',
                    'https://telemart.ua/office-equipment/']
    for catolog in list_catalog:
        print('\n ----------', catolog)
        response = requests.get(catolog, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='col-lg-3 col-md-4 b-category-box-item b-last-artics-list')
        for item in items:
            parser_page(item.find('a', 'b-inner').get('href'))


def parser_page(link_catalog): #Парсинг в каталоге
    page = 1
    while True:
        if page == 1:
            response = requests.get(link_catalog, headers=HEADERS)
        else:
            response = requests.get(f'{link_catalog}p{page}/', headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='b-i-product-inner')
        if len(items):
            print(page)
            for item in items:
                print(item.find('div', 'b-i-product-name').find('a').get('href'))
                parser_of_goods(item.find('div', 'b-i-product-name').find('a').get('href'))
            page += 1
        else:
            for ba_list in base_list:
                print(' '.join([i for i in ba_list]))
            print(f'Количество товаров: {len(base_list)}')
            return

parser_categories()
