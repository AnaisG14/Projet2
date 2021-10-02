import csv

class FileCsvModel:
    """ Model of file to save informations' book for each category"""

    def __init__(self, category_name):
        self.file_name = category_name
        self.file_type = "csv"
        self.file_to_create = f"FichiersCSV/{self.file_name}.{self.file_type}"

    def create_file_csv(self):
        with open(self.file_to_create, 'w', encoding="utf-8") as csvfile:
            fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                          'number_available', 'product_description', 'category', 'review_rating', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
