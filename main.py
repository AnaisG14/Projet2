import os
from Controllers import scrapper


if os.path.isdir("Images"):
    pass
else:
    os.mkdir("Images")
if os.path.isdir("FichiersCSV"):
    pass
else:
    os.mkdir("FichiersCSV")

scrap = scrapper.Scrapper()
scrap.start()
