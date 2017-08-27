import requests
from bs4 import BeautifulSoup, element

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

    def tags_only(self, html_list):
        tags = []
        for text in html_list:
            if isinstance(text, element.Tag):
                tags.append(text)
        return tags

    def get_tournament_bracket(self, year):
        url = self.get_tournament_urls(years_list=[year])[0]
        tree = self.get_tournament_tree_by_url(url)
        html_bracket = tree.find(id='brackets')

        games, teams, final_four = [], {}, []
        for bracket in ['east', 'south', 'west', 'midwest', 'national']:
            region_tree = html_bracket.find(id=bracket)
            for round_ in region_tree.find_all('div', 'round'):
                for game in self.tags_only(round_.contents):
                    g = self.tags_only(game.contents)
                    if len(g) >= 2:
                        teams[g[0].a.contents[0]] = g[0].a['href']
                        teams[g[1].a.contents[0]] = g[1].a['href']
                        game_link = (g[2].a['href'] if len(g) == 3 else "Game \
                                     link missing")
                        games.append((g[0].a.contents[0],
                                      g[1].a.contents[0],
                                      game_link))
                    else:
                        team = self.tags_only(game.contents)[0].a.contents[0]
                        final_four.append(team)
        return games, teams, final_four[:-1], final_four[-1]
