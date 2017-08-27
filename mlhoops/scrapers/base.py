import requests
from bs4 import BeautifulSoup, element


class Scraper():
    """
    Base class for web scrapers
    """
    def __init__(self, root_url, root_endpoint):
        self.root_url = root_url
        self.root_endpoint = root_endpoint

    def get_tree_by_url(self, url=None):
        if not url:
            url = self.root_endpoint
        res = requests.get(self.root_url + url)
        return BeautifulSoup(res.text, "html.parser")

    def tags_only(self, html_list):
        tags = []
        for text in html_list:
            if isinstance(text, element.Tag):
                tags.append(text)
        return tags
