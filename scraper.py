# -*-coding:utf-8-*-

# ============================== imports ==============================

import csv
import requests as rq
from bs4 import BeautifulSoup
import os

# ============================= fonctions =============================

def create_soup(url):
    """ Pick up html code in url and return a soup object"""
    page_content = rq.get(url, auth=('user', 'pass'))
    return BeautifulSoup(page_content.content, 'html.parser')


def get_information_book(url_book):
    """ Pick up information from url_book and extract information: title,
    upc, prices, review rating, number available, product description,
    image url and category.
    Save all informations in a dictionnary and return this dictionnary"""
    soup = create_soup(url_book)

    # pick up all information of the web site
    # pick up title
    title = soup.h1.string
    title_to_save = f"{sup_caractere_special(title)}.jpg"
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
    number_available = int(number_available_text.replace("In stock (", "").replace(" available)", ""))
    # pick up product description
    balises_p = soup.find_all("p")
    product_description = (balises_p[3]).string
    # pick up image url and category
    balises_a = soup.find_all("a")
    category = (balises_a[3]).string
    image_url = soup.img.get('src')
    image_url = (image_url.replace("../..", "http://books.toscrape.com"))

    # save all information in a dictionnary
    information_product = {"product_page_url": url_book,
                           "upc": upc, "title": title,
                           "price_including_tax": price_including_tax,
                           "price_excluding_tax": price_excluding_tax,
                           "number_available": number_available,
                           "product_description": product_description,
                           "category": category,
                           "review_rating": review_rating,
                           "image_url": image_url
                           }
    download_image(image_url, title_to_save)
    print(category)
    return information_product


def create_file_csv(filename):
    """ Create a file named filenamed with only the header line """
    # create file FichierCSV if it does not exist
    if os.path.isdir('FichiersCSV'):
        pass
    else:
        os.mkdir("FichiersCSV")

    with open(filename, 'w') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title',
                      'price_including_tax', 'price_excluding_tax',
                      'number_available', 'product_description',
                      'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def save_file_csv(filename, dicttosave):
    """ Save in filename.csv a dictionnary named dicttosave"""
    with open(filename, 'a') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title',
                      'price_including_tax', 'price_excluding_tax',
                      'number_available', 'product_description',
                      'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(dicttosave)


def get_all_pages(url_category):
    """ Return a list of all pages for one category"""
    list_url_in_one_category = [url_category]
    link_page = url_category
    while link_page:
        soup = create_soup(link_page)
        next_page = soup.select_one(".next > a")
        if next_page:
            link_page = f'{url_category.replace("index.html","")}{next_page.get("href")}'
            list_url_in_one_category.append(link_page)
        else:
            link_page = ""
    return list_url_in_one_category


def get_url_book(url_category):
    """ Return a list of url of all the books for url_category"""
    url_page_of_category = get_all_pages(url_category)
    list_url_book = []
    for url in url_page_of_category:
        soup = create_soup(url)
        list_img = soup.find_all("img", class_="thumbnail")
        # list_balises_parent = []
        for img in list_img:
            balise_parent = img.parent
            if balise_parent.name == "a":
                book_url = balise_parent.get('href')
                book_url = book_url[9:]
                book_url = f"http://books.toscrape.com/catalogue/{book_url}"
                list_url_book.append(book_url)
            # list_balises_parent.append(balise_parent)
    return list_url_book


def get_url_category():
    """ Return a list of all url category of the site http://books.toscrape.com/"""
    soup = create_soup('http://books.toscrape.com/')
    sidebar_category = soup.find("div", class_="side_categories")
    links_url_category = sidebar_category.find_all("a")
    categories_url_name = []
    for link in links_url_category:
        category_name = sup_caractere_special(link.string)
        url_name = (f"http://books.toscrape.com/{link.get('href')}", category_name)
        categories_url_name.append(url_name)
    del categories_url_name[0]
    return categories_url_name


def sup_caractere_special(text):
    """retourne le texte sans les caractères spéciaux : .:/\n et espaces
    afin de les utiliser comme nom de fichier.
    """
    caracteres_speciaux = [".", "/", ":", "\n", " "]
    for car in caracteres_speciaux:
        if car in text:
            text = text.replace(car, "")
    return text


def download_image(url, title):
    """ Download an image and save it as its title book"""
    # create file Images if it does not exist
    if os.path.isdir("Images"):
        pass
    else:
        os.mkdir("Images")
    # save image
    url_image = (rq.get(url)).content
    with open(f"Images/{title}", 'wb') as f:
        f.write(url_image)
    print(f"Image downloaded as {title}")


def save_informations_all_books(categories_url_name):
    """ For each url_categoru, save all information book in
    one file for one category
    """
    # return list of url for each book of the category
    categories_url_name = categories_url_name
    for item in categories_url_name:
        url_book = get_url_book(item[0])
        category = item[1]
        # return a list of all dictionnary of information for one book
        list_informations_books = []
        for url in url_book:
            info_book = get_information_book(url)
            list_informations_books.append(info_book)
        category = f"FichiersCSV/{category}.csv"
        create_file_csv(category)
        for book in list_informations_books:
            save_file_csv(category, book)


def scraper():
    """ Scrapping of the site "https://books.toscrape.com :
        - get all url of categories of the site,
        - get all url of all books for each category
        - scrap each book and save in file.csv : product_page_url, upc,
        title, price_including_tax,price_excluding tax, number available,
        product_description, category, review_rating, image_url
        - download image for each book.
        At the end of the scrapping, you must have 2 new directories named
        "Fichiers.csv" and "Images" contend one file.csv for each category
        and all images.
        """
    categories_url_name = get_url_category()
    save_informations_all_books(categories_url_name)

# ============================ main project ============================

if __name__ == '__main__':
    scraper()
