from Models import scrap_model, book_model

class GetInformationBook:
    """ Get information book and modify Book"""

    def __init__(self, url_books):
        self.url_books = url_books

    def __call__(self):
        for category, urls in self.url_books.items():
            for url_book in urls:
                book_scrapped = scrap_model.ScrapModel(url_book)
                informations_book = book_scrapped.information_product
                book = book_model.BookModel(informations_book)
                book.save_informations()
                book.download_image()
        return
