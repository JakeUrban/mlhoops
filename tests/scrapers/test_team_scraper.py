from mlhoops.scrapers import TeamScraper


endpoints = ['/cbb/schools/gonzaga/2017.html',
             '/cbb/schools/north-carolina/2016.html']


def test_team_info():
    ts = TeamScraper()
    for endpoint in endpoints:
        team_info = ts.get_team_info(endpoint)
        assert None not in team_info


def test_player_info():
    ts = TeamScraper()
    for endpoint in endpoints:
        headers, players = ts.get_player_info(endpoint)
        assert len(headers)-1 == len(list(players.items())[0][1])
