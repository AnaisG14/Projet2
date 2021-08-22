# -*-coding:utf-8-*-
import csv
import requests as rq
from bs4 import BeautifulSoup

def createSoup(url):
    """ Pick up html code in url and return a soup object"""
    page_content = rq.get(url, auth=('user', 'pass'))
    return BeautifulSoup(page_content.content, 'html.parser')

def getInformationBook(url_book):
    """ Pick up information from url_book and extract information."""
    soup = createSoup(url_book)

    # pick up all information of the web site
    title = soup.h1.string     # pick up title
    table_balises = soup.find_all("td") # pick up upc, prices, review rating, number available
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

    balises_p = soup.find_all("p")      # pick up product description
    product_description = (balises_p[3]).string

    balises_a = soup.find_all("a")      # pick up image url and category
    category = (balises_a[3]).string
    image_url = (soup.img).get('src')

    # save all information in a dictionnary
    information_product = {}
    information_product["product_page_url"] = url_book
    information_product["upc"] = upc
    information_product["title"] = title
    information_product["price_including_tax"] = price_including_tax
    information_product["price_excluding_tax"] = price_excluding_tax
    information_product["number_available"] = number_available
    information_product['product_description'] = product_description
    information_product['category'] = category
    information_product['review_rating'] = review_rating
    information_product["image_url"] = image_url
    return information_product

def createFielcsv(filename):
    with open(filename, 'w') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                      'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def saveFilecsv(filename, dicttosave):
    """ Save in filename.csv a dictionnary named dicttosave"""
    with open(filename, 'a') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                      'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(dicttosave)

def getAllPages(url_category):
    """ Return a list of url of all page for one category even if category contains more than 20 books"""
    soup = createSoup(url_category)
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
        list_url = [url_category]
    return list_url

def getUrlBook(url_category):
    """ Return a list of url of all the books for url_category"""
    soup = createSoup(url_category)
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

def getUrlCategory():
    """ Return a list of all url category of the site http://books.toscrape.com/"""
    soup = createSoup('http://books.toscrape.com/')
    sidebar_category = soup.find("div", class_="side_categories")
    links_url_category = sidebar_category.find_all("a")
    urls_category = []
    names_category = []
    for link in links_url_category:
        urls_category.append(link.get('href'))
        names_category.append(link.string)
    urls_category1 = []
    for link in urls_category:
        urls_category1.append('http://books.toscrape.com/' + link)
    del urls_category1[0]
    del names_category[0]
    names_category = [name.replace("\n", "") for name in names_category]
    names_category = [name.replace(" ", "") for name in names_category]
    return urls_category1, names_category

################### main project ######################################################
if __name__ == '__main__':
    # 2 exemples de liens de catégorie
    url_category1 = 'http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html'
    url_category2 = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"

    # return list of url of all category
    categories_url_name = getUrlCategory()
    categories_url = categories_url_name[0]
    categories_name = categories_url_name[1]

    # for each category, return a dictionnary with cle:all pages category, element: url books of category
    dict_categories = {}
    i = 0
    for url in categories_url:
        dict_categories[categories_name[i]] = getAllPages(categories_url[i])
        i += 1

    # return list of url for each book of the category
    for category, urls in dict_categories.items():
        url_all_books_in_category = []
        for url in urls:
            url_book= getUrlBook(url)
            for url in url_book:
                url_all_books_in_category.append(url)
        # return a list of all dictionnary of information for one book
        list_informations_books = []
        for url in url_all_books_in_category:
            info_book = getInformationBook(url)
            list_informations_books.append(info_book)
        category = category + ".csv"
        createFielcsv(category)
        for book in list_informations_books:
            saveFilecsv(category, book)

