from datetime import datetime

from mlhoops.scrapers.base import ScraperBase
from mlhoops.util.game_util import get_game_stats_file


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
        html = self.get_html_by_url(endpoint)
        tables_html = html.find(id='boxes').find_all('table', 'stats_table')
        tables, players = [], {}
        for idx, t in enumerate(tables_html):
            h_row = t.thead.tr.next_sibling.next_sibling
            headers = [header['aria-label'] for header in h_row.contents[1::2]]
            tables.append([headers])
            for tr in t.tbody.contents[1::2]:
                if ((tr.get('class') and tr['class'] == 'thead') or
                    tr.th.get('aria-label')):
                    continue
                players[tr.th.a.contents[0]] = {'endpoint': tr.th.a['href']}
                row = []
                for td in tr.contents[1:]:
                    row.append(td.contents[0] if td.contents else None)
                tables[idx].append(row)
        return tables, players
