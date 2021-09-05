# -*-coding:utf-8-*-
import csv


def create_file_csv(filename):
    with open(filename, 'w', encoding="utf-8") as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                      'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def save_file_csv(filename, dicttosave):
    """ Save in filename.csv a dictionnary named dicttosave"""
    with open(filename, 'a', encoding="utf-8") as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                      'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(dicttosave)
