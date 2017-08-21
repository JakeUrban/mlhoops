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
        self.root_url = 'https://www.sports-reference.com'
        self.root_endpoint = '/cbb/postseason'
        self.current_year = datetime.utcnow().year

    def root_source_tree(self):
        res = requests.get(self.root_url + self.root_endpoint)
        return BeautifulSoup(res.text, "html.parser")

    def get_tournament_urls(self, num_years=None, years_list=None):
        rows = self.root_source_tree().find('tbody').contents[1::2]
        if years_list:
            urls = []
            for year in years_list:
                idx = self.current_year - year
                urls.append(rows[idx].th.a.get('href'))
            return urls
        elif num_years:
            return [row.th.a.get('href') for row in rows[:num_years]]
        else:
            raise InputError("Method takes either num_years or year_list \
                              argument")

    def get_tournament_tree_by_url(self, url):
        res = requests.get(self.root_url + url)
        return BeautifulSoup(res.text, "html.parser")

    def get_tournament_bracket(self, year):
        url = self.get_tournament_urls(years_list=[year])[0]
        tree = self.get_tournament_tree_by_url(url)
        return tree.find(id='brackets').contents
