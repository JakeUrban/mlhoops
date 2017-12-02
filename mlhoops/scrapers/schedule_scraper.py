from mlhoops.scrapers.base import ScraperBase


class ScheduleScraper(ScraperBase):
    """
    Web scraper for https://www.sports-reference.com/cbb/seasons/
    """
    def __init__(self):
        super(ScheduleScraper, self).__init__(
            'https://www.sports-reference.com')
        self.root_endpoint = '/cbb/seasons/{}-school-stats.html'

    def get_schedule(self, team_endpoint, only_season=False):
        """
        Given endpoint for team schedule, return the links to the games
        played in chronological order.

        Example endpoint: /cbb/schools/oregon/2017-schedule.html
        """
        html = self.get_html_by_url(team_endpoint[:-5] + '-schedule.html')
        games = []
        for row in self.tags_only(html.find(id='schedule').tbody.contents):
            tags = self.tags_only(row.contents)
            if hasattr(row.td, 'a') and tags[6].a:
                if not only_season:
                    games.append(row.td.a['href'])
                elif only_season and tags[4].get_text() != 'NCAA':
                    games.append(row.td.a['href'])
        return games

    def get_team_urls(self, year):
        """
        Given a year, return links and names to all teams who participated in that
        """
        html = self.get_html_by_url(self.root_endpoint.format(year))
        table = html.find(id='basic_school_stats')
        urls = []
        for row in self.tags_only(table.tbody.contents):
            if not row.get('class'):
                urls.append(row.td.a['href'])
        return urls
