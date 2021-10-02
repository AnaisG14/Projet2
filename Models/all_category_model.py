from utils import create_soup, sup_caractere_special, get_all_pages


class AllCategoryModel:
    """ get on the site a list of a tuple contained urls of the category
    and the name of the category"""

    def __init__(self, url_site):
        self.url_site = url_site
        self.categories_url_name = []

    def get_url_of_categories(self):
        """ get all url of a category """
        soup = create_soup.CreateSoup(self.url_site)
        soup = soup.html_parser()
        sidebar_category = soup.find("div", class_="side_categories")
        links_url_category = sidebar_category.find_all("a")
        for link in links_url_category:
            category_name = sup_caractere_special.sup_caractere_special(link.string)
            main_url_category = f"http://books.toscrape.com/{link.get('href')}"
            all_url_category = get_all_pages.get_all_pages(main_url_category)
            url_name = (all_url_category, category_name)
            self.categories_url_name.append(url_name)
        del self.categories_url_name[0]
        return