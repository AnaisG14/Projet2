class DisplayWorkingScrapper:
    """ Display the progression of the scrapping"""

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Image downloaded as {self.title}"
