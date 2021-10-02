from Models import all_category_model
from Controllers import create_file_csv

class GetUrlCategories:
    """ get url of all the categories af the site"""

    def __init__(self):
        pass

    def __call__(self):
        """ create a list of all urls' categories"""
        print("recherche des catégories")
        category = all_category_model.AllCategoryModel('http://books.toscrape.com/')
        category.get_url_of_categories()
        return create_file_csv.CreateFileCSV(category.categories_url_name)