from utils import create_soup

def get_all_pages(url_category):
    """ Return a list of all pages for one category"""
    list_url_in_one_category = [url_category]
    link_page = url_category
    while link_page:
        soup = create_soup.CreateSoup(link_page)
        soup = soup.html_parser()
        next_page = soup.select_one(".next > a")
        if next_page:
            link_page = f'{url_category.replace("index.html","")}{next_page.get("href")}'
            list_url_in_one_category.append(link_page)
        else:
            link_page = ""
    return list_url_in_one_category