import requests
from bs4 import BeautifulSoup

from datetime import datetime


class InputError(Exception):
    """
    Exception class for incorrect input
    """
    def __init__(self, message):
        self.message = message


class TournamentScraper():
    """
    Web scraper for https://www.sports-reference.com/cbb/postseason/
    """
    def __init__(self):
        self.root_url = 'https://www.sports-reference.com/cbb/postseason'
        self.current_year = datetime.utcnow().year

    def root_source_tree(self):
        res = requests.get(self.root_url)
        return BeautifulSoup(res.text, "html.parser")

    def get_tournament_urls(self, num_years=10, years_list=None):
        root_tree = self.root_source_tree()
        rows = root_tree.body.tbody.contents[1::2]
        if years_list:
            urls = []
            for year in years_list:
                idx = self.current_year - year
                urls.append(rows[idx].th.a.get('href'))
            return urls
        elif num_years:
            return [row.th.a.get('href') for row in rows[:num_years]]
        else:
            raise InputError("method takes either num_years or year_list")

    def get_tournament_tree_by_url(self, url):
        res = requests.get(self.root_url + url)
        return BeautifulSoup(res.text, "html.parser")
