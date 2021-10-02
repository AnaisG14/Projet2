from Controllers import get_url_category as guc

class Scrapper:
    def __init__(self):
        self.controller = None

    def start(self):
        self.controller = guc.GetUrlCategories()
        while self.controller:
            self.controller = self.controller()
