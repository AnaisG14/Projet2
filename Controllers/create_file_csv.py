from Models import file_csv_model
from Controllers import get_url_book

class CreateFileCSV:
    """ Create a new file for each category """

    def __init__(self, categories_url_name):
        self.categories_url_name = categories_url_name
        self.category_name = []
        for item in self.categories_url_name:
            self.category_name.append(item[1])

    def __call__(self):
        for category in self.category_name:
            category_file = file_csv_model.FileCsvModel(category)
            category_file.create_file_csv()
        return get_url_book.GetUrlBooks(self.categories_url_name)
