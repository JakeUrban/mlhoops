from mlhoops.scrapers.base import ScraperBase


class TeamScraper(ScraperBase):
    """
    Web scraper for https://www.sports-reference.com team pages
    """
    def __init__(self, team_endpoints=None):
        super(TeamScraper, self).__init__(
            'https://www.sports-reference.com')
        self.team_endpoints = team_endpoints

    def get_team_info(self, endpoint):
        html = self.get_html_by_url(endpoint)
        record_p = html.find(id='meta').div.next_sibling.next_sibling.p
        wins, losses = record_p.contents[1].strip().split()[0].split('-')
        team_opp_html = html.find(id='team_stats')
        team_opp_headers = []
        for th in self.tags_only(team_opp_html.tr.contents)[3:]:
            team_opp_headers.append(th['aria-label'])
        team_opp = [team_opp_headers]
        for idx, tr in enumerate(self.tags_only(team_opp_html.contents)[2::2]):
            team_opp_row = []
            for td in self.tags_only(tr)[3:]:
                data = td.contents[0] if td.contents else None
                team_opp_row.append(data)
            team_opp.append(team_opp_row)
        return wins, losses, team_opp

    def get_player_info(self, team_endpoint):
        html = self.get_html_by_url(team_endpoint)
        per_game_html = html.find(id='per_game')
        per_game_headers = []
        for th in self.tags_only(per_game_html.thead.tr.contents)[1:]:
            per_game_headers.append(th['aria-label'])
        players = {}
        for tr in self.tags_only(per_game_html.tbody.contents):
            player_row, player_name = [], None
            for idx, td in enumerate(self.tags_only(tr)[1:]):
                if idx == 0:
                    player_name = td.a.contents[0]
                else:
                    data = td.contents[0] if td.contents else None
                    player_row.append(data)
            players[player_name] = player_row
        return players
