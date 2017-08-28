from datetime import datetime

from mlhoops.scrapers.base import ScraperBase


class GameScraper(ScraperBase):
    """
    Web scraper for https://www.sports-reference.com game pages
    """
    def __init__(self, game_endpoints=None):
        super(GameScraper, self).__init__(
            'https://www.sports-reference.com')
        self.game_endpoints = game_endpoints

    def get_game_info(self, endpoint, game=None):
        g = game if isinstance(game, list) else []
        html = self.get_html_by_url(endpoint)
        sb = html.find('div', 'scorebox')
        if not g:
            t1_name = sb.div.div.strong.a.contents[0]
            t2_name = sb.div.next_sibling.next_sibling.div.strong.a.contents[0]
            g.extend((t1_name, t2_name, endpoint))
        score = sb.find_all('div', 'score')
        t1_score = int(score[0].contents[0])
        t2_score = int(score[1].contents[0])
        date_str = sb.find('div', 'scorebox_meta').div.contents[0]
        date = datetime.strptime(date_str, '%B %d, %Y')
        g.extend((t1_score, t2_score, date))
        return g

    def get_game_stats(self, endpoint):
        pass
