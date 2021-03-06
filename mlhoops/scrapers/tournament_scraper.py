from datetime import datetime

from bs4 import BeautifulSoup, element  # noqa
import requests  # noqa

from mlhoops.scrapers.base import ScraperBase


class TournamentScraper(ScraperBase):
    """
    Web scraper for https://www.sports-reference.com/cbb/postseason/
    """
    def __init__(self):
        super(TournamentScraper, self).__init__(
            'https://www.sports-reference.com',
            '/cbb/postseason')
        self.current_year = datetime.utcnow().year

    def get_tournament_urls(self, num_years=None, years_list=None):
        rows = self.get_html_by_url().find('tbody').contents[1::2]
        if years_list:
            urls = []
            for year in years_list:
                idx = self.current_year - year
                urls.append(rows[idx].th.a.get('href'))
            return urls
        elif num_years:
            return [row.th.a.get('href') for row in rows[:num_years]]
        else:
            raise Exception("Method takes either num_years or year_list \
                             argument")

    def add_game(self, g, games, teams, bracket):
        if g[0].a.contents[0] not in teams:
            seed = (g[0].span.contents[0] if len(g[0].span.contents) > 0
                    else "Seed number missing")
            teams[g[0].a.contents[0]] = [g[0].a['href'], seed, bracket]
        if g[1].a.contents[0] not in teams:
            seed = (g[1].span.contents[0] if len(g[1].span.contents) > 0
                    else "Seed number missing")
            teams[g[1].a.contents[0]] = [g[1].a['href'], seed, bracket]
        game_link = g[2].a['href'] if len(g) == 3 else "Game link missing"
        games.append([g[0].a.contents[0], g[1].a.contents[0], game_link])

    def get_tournament_info(self, year):
        url = self.get_tournament_urls(years_list=[year])[0]
        html = self.get_html_by_url(url)
        html_bracket = html.find(id='brackets')

        brackets = []
        for bracket in self.tags_only(html_bracket):
            brackets.append(bracket['id'])

        games, teams, final_four = [], {}, []
        for bracket in brackets:
            region_tree = html_bracket.find(id=bracket)
            for round_ in region_tree.find_all('div', 'round'):
                for game in self.tags_only(round_.contents):
                    g = self.tags_only(game.contents)
                    if len(g) >= 2 and g[0].a and g[1].a:
                        self.add_game(g, games, teams, bracket)
                    elif len(g) >= 2 and not (g[0].a and g[1].a):
                        continue  # pragma: no cover
                    else:
                        final_four.append(g[0].a.contents[0])

        return games, teams, final_four[:-1], final_four[-1]
