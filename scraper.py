# -*-coding:utf-8-*-
import os
from save_files import create_file_csv, save_file_csv
from get_url_book import get_url_book, get_url_category
from scrapabook import get_information_book



def save_category(categories_url_name):
    """ For each url_categoru, save all information book in one file for one category"""
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
        print(f"save file {category}")
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
    save_category(categories_url_name)


# ============================ main project =====================


if __name__ == '__main__':
    if os.path.isdir("Images"):
        pass
    else:
        os.mkdir("Images")
    if os.path.isdir("FichiersCSV"):
        pass
    else:
        os.mkdir("FichiersCSV")
    scraper()
