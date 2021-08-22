# -*-coding:utf-8-*-
import scrapabook as scb
import requests as rq
from bs4 import BeautifulSoup

def getAllPages(url_category):
    """ Get all page for one category if category contains more than 20 books"""
    soup = scb.createSoup(url_category)
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

def getUrlBook(url_category):
    """ Return a list of url of all the books for url_category"""
    soup = scb.createSoup(url_category)
    list_img = soup.find_all("img", class_="thumbnail")
    list_balises_parent = []
    list_url_book = []
    for img in list_img:
        balise_parent = img.parent
        if balise_parent.name == "a":
            book_url = (balise_parent).get('href')
            book_url = book_url[9:]
            list_url_book.append(book_url)
        list_balises_parent.append(balise_parent)
    i = 0
    for url in list_url_book:
        list_url_book[i] = "http://books.toscrape.com/catalogue/" + url
        i += 1
    return list_url_book

if __name__ == '__main__':
    url_category1 = 'http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html'
    url_category2 = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"

    list_url = getAllPages(url_category2)
    url_all_books_in_category = []
    for url in list_url:
        url_book= getUrlBook(url)
        for url in url_book:
            url_all_books_in_category.append(url)
    print(url_all_books_in_category)

    for url in url_all_books_in_category:
        info_book = scb.getInformationBook(url)
        print(info_book)