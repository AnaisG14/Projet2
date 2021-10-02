from utils import create_soup
from Controllers import get_information_book

class GetUrlBooks:
    """ get url of all books for one category"""
    def __init__(self, categories_url_name):
        self.url_books = {}
        for item in categories_url_name:
            category = item[1]
            urls = []
            for url in item[0]:
                soup = create_soup.CreateSoup(url)
                soup = soup.html_parser()
                list_img = soup.find_all("img", class_="thumbnail")
                for img in list_img:
                    balise_parent = img.parent
                    if balise_parent.name == "a":
                        book_url = balise_parent.get('href')
                        book_url = book_url[9:]
                        book_url = f"http://books.toscrape.com/catalogue/{book_url}"
                        urls.append(book_url)
            self.url_books[category] = urls

    def __call__(self):
        print("recherche des urls dans les catégories suivantes")
        return get_information_book.GetInformationBook(self.url_books)
