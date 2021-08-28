# -*-coding:utf-8-*-
import requests as rq
from utils import create_soup, sup_caractere_special


def get_information_book(url_book):
    """ Pick up information from url_book and extract information."""
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
                           "upc": upc,
                           "title": title,
                           "price_including_tax": price_including_tax,
                           "price_excluding_tax": price_excluding_tax,
                           "number_available": number_available,
                           'product_description': product_description,
                           'category': category,
                           'review_rating': review_rating,
                           "image_url": image_url}
    download_image(image_url, title_to_save)
    print(f"catégorie: {category}")
    return information_product


def download_image(url, title):
    """ Download an image and save it as its title book"""
    url_image = (rq.get(url)).content
    with open(f"Images/{title}", 'wb') as f:
        f.write(url_image)
    print(f"Image downloaded as {title}")
