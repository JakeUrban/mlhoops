import pytest
from mlhoops.scrapers import TournamentScraper


@pytest.mark.parametrize('num_years, years_list',
                         [(3, None), (None, [2014, 2013, 2012]), (None, None)])
def test_tournament_urls(num_years, years_list):
    ts = TournamentScraper()
    if num_years or years_list:
        urls = ts.get_tournament_urls(num_years=num_years,
                                      years_list=years_list)
        assert len(urls) == 3
    else:
        with pytest.raises(Exception):
            ts.get_tournament_urls()


years = [2017, 2016, 2015, 2014]


def test_get_tournament_info():
    ts = TournamentScraper()
    for year in years:
        games, teams, final_four, champion = ts.get_tournament_info(year)
        assert len(games) == 63 and len(teams) == 64
        assert len(final_four) == 4 and champion in final_four
