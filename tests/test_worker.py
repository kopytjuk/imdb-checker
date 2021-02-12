import pytest

from logic.worker import check_imdb_user_watchlist, check_top_250_movies
from logic.watchlist_provider import WatchlistError


WATCHLISTS = [
    "https://www.imdb.com/user/ur58171394/watchlist",
    #"https://www.imdb.com/user/ur5205364/watchlist",  # large
    #"https://www.imdb.com/user/ur85031360/watchlist",
]

LOCATIONS = [
    "de_DE",
    #"en_GB",
    #"en_US"
]


@pytest.mark.parametrize("location_code", LOCATIONS)
@pytest.mark.parametrize("url", WATCHLISTS)
def test_imdb_user_watchlist(url: str, location_code: str):

    results = check_imdb_user_watchlist(url, location_code, None)

    assert len(results) > 0


@pytest.mark.parametrize("location_code", LOCATIONS)
def test_imdb_top_250_movies(location_code: str):

    results = check_top_250_movies(location_code)
    assert len(results) > 200
    assert len(results) == 250
