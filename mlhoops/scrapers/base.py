import requests
from bs4 import BeautifulSoup, element


class ScraperBase():
    """
    Base class for web scrapers
    """
    def __init__(self, root_url, root_endpoint=None):
        self.root_url = root_url
        self.root_endpoint = root_endpoint

    def get_html_by_url(self, url=None):
        if not url:
            url = self.root_endpoint if hasattr(self, 'root_endpoint') else ''
        res = requests.get(self.root_url + url)
        return BeautifulSoup(res.text, "html.parser")

    def tags_only(self, html):
        tags = []
        for text in html:
            if isinstance(text, element.Tag):
                tags.append(text)
        return tags
