import csv
import requests as rq
from utils import sup_caractere_special
from Views import display_working_scrapper

class BookModel:
    """ information about books of the site"""
    def __init__(self, dict_informations):
        self.informations_book = dict_informations
        self.product_page_url = dict_informations["product_page_url"]
        self.upc = dict_informations["upc"]
        self.title = dict_informations["title"]
        self.title_to_save = f"{sup_caractere_special.sup_caractere_special(dict_informations['title'])}.jpg"
        self.price_including_tax = dict_informations["price_including_tax"]
        self.price_excluding_tax = dict_informations["price_excluding_tax"]
        self.number_available = dict_informations["number_available"]
        self.product_description = dict_informations["product_description"]
        self.category = dict_informations["category"]
        self.review_rating = dict_informations["review_rating"]
        self.image_url = dict_informations["image_url"]

    def save_informations(self):
        """ save information in a csv file"""
        file_to_save = f"FichiersCSV/{self.category}.csv"
        with open(file_to_save, 'a', encoding="utf-8") as csvfile:
            fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                          'number_available', 'product_description', 'category', 'review_rating', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(self.informations_book)

    def download_image(self):
        """ download_image of book"""
        image_url = (rq.get(self.image_url)).content
        with open(f"Images/{self.title_to_save}", 'wb') as f:
            f.write(image_url)
        in_process = display_working_scrapper.DisplayWorkingScrapper(self.title)
        print(in_process)
