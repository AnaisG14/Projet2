# -*-coding:utf-8-*-
import requests as rq
from bs4 import BeautifulSoup


def create_soup(url):
    """ Pick up html code in url and return a soup object"""
    page_content = rq.get(url, auth=('user', 'pass'))
    return BeautifulSoup(page_content.content, 'html.parser')


def sup_caractere_special(text):
    """retourne le texte sans les caractères spéciaux : .:/\n et espaces afin de les utiliser
    comme nom de fichier"""
    caracteres_speciaux = [".", "/", ":", "\n", " "]
    for car in caracteres_speciaux:
        if car in text:
            text = text.replace(car, "")
    return text
