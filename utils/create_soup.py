from bs4 import BeautifulSoup
import requests as rq


class CreateSoup:
    """ Pick up html code in url and return a soup object"""

    def __init__(self, url):
        self.page_content = rq.get(url, auth=('user', 'pass'))

    def html_parser(self):
        return BeautifulSoup(self.page_content.content, 'html.parser')
