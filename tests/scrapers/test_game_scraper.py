from mlhoops.scrapers import GameScraper


endpoints = ['/cbb/boxscores/2017-03-16-villanova.html',
             '/cbb/boxscores/2017-03-19-duke.html',
             '/cbb/boxscores/2017-04-03-north-carolina.html']


def test_game_scraper_info():
    gs = GameScraper()
    for endpoint in endpoints:
        info = gs.get_game_info(endpoint)
        assert len(info) == 5
        assert None not in info and '' not in info
        assert info[-1].strftime('%Y-%m-%d') in endpoint.split('/')[-1]


def test_game_stats():
    gs = GameScraper()
    for endpoint in endpoints:
        tables = gs.get_game_stats(endpoint)
        assert len(tables) == 2
