import pytest

from logic.main import check_imdb_user_watchlist, check_medialist
from logic.config import default_config


WATCHLISTS = [
    "https://www.imdb.com/user/ur58171394/watchlist",
    "https://www.imdb.com/user/ur5205364/watchlist",  # large
    "https://www.imdb.com/user/ur85031360/watchlist",
]

LOCATIONS = [
    "de_DE",
    "en_GB",
    "en_US"
]

default_config.request_cooldown_time = 0.2


@pytest.mark.parametrize("location_code", LOCATIONS)
@pytest.mark.parametrize("url", WATCHLISTS)
def test_imdb_user_watchlist(url: str, location_code: str):

    results = check_imdb_user_watchlist(url, location_code, None)

    assert len(results) > 0


@pytest.mark.parametrize("location_code", LOCATIONS)
def test_imdb_top_250_movies(location_code: str):

    results = check_medialist("imdb_top_250", location_code)
    assert len(results) > 200
    assert len(results) == 250
