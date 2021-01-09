from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from dateutil import parser
from decimal import *


def get_release_date(text):
    parts = text.split()
    date = parser.parse(f"{parts[-3]} {parts[-2]} {parts[-1]}")
    return date.strftime("%d-%m-%Y")


def format_price(price):
    return Decimal(price.strip('£'))


def get_latest_stock_additions():
    source = requests.get("https://www.masterofmalt.com/new-arrivals/whisky-new-arrivals/").text

    soup = BeautifulSoup(source, 'html.parser')
    content = soup.find('div', {'id': 'productBoxWideContainer'})
    stock = {'date': get_release_date(content.div.find('p').text), 'whiskies': []}

    for line in content:
        if isinstance(line, NavigableString):
            continue
        if isinstance(line, Tag):
            if line.has_attr('data-name'):
                distillery = line.find('a', {'class': 'product-box-wide-distillery'})
                price = line.find('div', {'class': 'product-box-wide-price'})

                stock['whiskies'].append({
                    'id': line.attrs['data-productid'],
                    'name': line.attrs['data-name'],
                    'distillery': distillery.text,
                    'url': line.attrs['data-product-url'],
                    'price': format_price(price.text) if price else "unknown"
                })
            else:
                if len(stock['whiskies']) == 0:
                    continue
                else:
                    break

    return stock


def display_stock(stock):
    print(stock['date'])
    for whiskey in stock['whiskies']:
        print(f"{whiskey['distillery']} - {whiskey['name']} - {whiskey['price']}")
