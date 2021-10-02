from utils import create_soup

class ScrapModel:
    def __init__(self, url_book):
        self.url_book = url_book
        self.information_product = {}

        """ Pick up information from url_book and extract information."""
        soup = create_soup.CreateSoup(self.url_book)
        soup = soup.html_parser()
        # pick up title
        title = soup.h1.string
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
        self.information_product = {"product_page_url": self.url_book,
                           "upc": upc,
                           "title": title,
                           "price_including_tax": price_including_tax,
                           "price_excluding_tax": price_excluding_tax,
                           "number_available": number_available,
                           'product_description': product_description,
                           'category': category,
                           'review_rating': review_rating,
                           "image_url": image_url}

