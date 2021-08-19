# -*-coding:utf-8-*-
import requests as rq
from bs4 import BeautifulSoup

def getPage(url):
    """ pick up a page wich we know url"""
    req = rq.get(url, auth=('user', 'pass'))
    return req

# liens vers quelques pages test
product_page_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
product_page_url1 = 'http://books.toscrape.com/catalogue/in-a-dark-dark-wood_963/index.html'
product_page_url2 = 'http://books.toscrape.com/catalogue/the-stranger_861/index.html'
product_page_url3 = 'http://books.toscrape.com/catalogue/sophies-world_966/index.html'


# pick up all information of the web site
page = getPage(product_page_url3)
soup = BeautifulSoup(page.content, 'html.parser')

# pick up title
title = soup.h1.string

# pick up upc, prices, review rating, number available
table_balises = soup.find_all("td")
table_contenus = []
for contenu in table_balises:
    table_contenus.append(contenu.string)
upc = table_contenus[0]
price_excluding_tax = table_contenus[2]
price_excluding_tax = float(price_excluding_tax[1:])
price_including_tax = table_contenus[3]
price_including_tax = float(price_including_tax[1:])
review_rating = int(table_contenus[6])
number_available_text = table_contenus[5]
number_available = "0"
for car in number_available_text:
    if car in ["0","1","2","3","4","5","6","7","8","9"]:
        number_available += car
number_available = int(number_available)

# pick up product description
balises_p = soup.find_all("p")
product_description = (balises_p[3]).string

# pick up image url
balises_a = soup.find_all("a")
category = (balises_a[3]).string
image_url= (soup.img).get('src')

# save all information in a dictionnary
information_product = {}
information_product["product_page_url"] = product_page_url
information_product["upc"] = upc
information_product["title"] = title
information_product["price_including_tax"] = price_including_tax
information_product["price_excluding_tax"] = price_excluding_tax
information_product["number_available"] = number_available
information_product['product_description'] = product_description
information_product['category'] = category
information_product['review_rating'] = review_rating
information_product["image_url"] = image_url

for cle, value in information_product.items():
    print(f"{cle} : {value}")



