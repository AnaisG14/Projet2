# -*-coding:utf-8-*-
import scrapabook as scb
import requests as rq
from bs4 import BeautifulSoup

url_category1 = 'http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html'
url_category2 = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
def getAllPages(url_category):
    """ Get all page for one category if category contains more than 20 books"""
    page = rq.get(url_category, auth=('user', 'pass'))
    soup = BeautifulSoup(page.content, 'html.parser')
    number_of_page = soup.find_all("li", class_="current")
    if number_of_page:
        current_page = (number_of_page[0]).string
    else:
        current_page = ""
    if current_page:
        number = 0
        for car in current_page:
            if car in ["0","1","2","3","4","5","6","7","8","9"]:
                number = int(car)
        list_url = []
        for i in range(number):
            list_url.append(url_category[:-10] + "page-" + str(i+1) + ".html")
    else:
        list_url = [url_category1]
    return list_url

a = getAllPages(url_category1)
b = getAllPages(url_category2)
print(a)
print(b)

def getUrlBook(url_category):
    pass

product_page_url3 = 'http://books.toscrape.com/catalogue/sophies-world_966/index.html'
info_book = scb.getInformationBook(product_page_url3)
print(info_book)