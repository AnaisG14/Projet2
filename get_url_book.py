# -*-coding:utf-8-*-
from utils import create_soup, sup_caractere_special


def get_url_book(url_category):
    """ Return a list of url of all the books for url_category"""
    url_page_of_category = get_all_pages(url_category)
    list_url_book = []
    for url in url_page_of_category:
        soup = create_soup(url)
        list_img = soup.find_all("img", class_="thumbnail")
        # list_balises_parent = []
        for img in list_img:
            balise_parent = img.parent
            if balise_parent.name == "a":
                book_url = balise_parent.get('href')
                book_url = book_url[9:]
                book_url = f"http://books.toscrape.com/catalogue/{book_url}"
                list_url_book.append(book_url)
            # list_balises_parent.append(balise_parent)
    return list_url_book


def get_url_category():
    """ Return a list of all url category of the site http://books.toscrape.com/"""
    soup = create_soup('http://books.toscrape.com/')
    sidebar_category = soup.find("div", class_="side_categories")
    links_url_category = sidebar_category.find_all("a")
    categories_url_name = []
    for link in links_url_category:
        category_name = sup_caractere_special(link.string)
        url_name = (f"http://books.toscrape.com/{link.get('href')}", category_name)
        categories_url_name.append(url_name)
    del categories_url_name[0]
    return categories_url_name


def get_all_pages(url_category):
    """ Return a list of all pages for one category"""
    list_url_in_one_category = [url_category]
    link_page = url_category
    while link_page:
        soup = create_soup(link_page)
        next_page = soup.select_one(".next > a")
        if next_page:
            link_page = f'{url_category.replace("index.html","")}{next_page.get("href")}'
            list_url_in_one_category.append(link_page)
        else:
            link_page = ""
    return list_url_in_one_category
