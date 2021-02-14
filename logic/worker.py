"""Main entry point for each celery worker (process). Each function outputs a list of
datatypes.Results object
"""

from .datatypes import Results
from .imdb_provider import get_top_250, IMDbWatchlistGetter
from .availability import check_availability


def check_imdb_user_watchlist(watchlist_url: str, location_code: str,
                              progress_tracker=None) -> Results:

    if "www.imdb.com" in watchlist_url:
        wp = IMDbWatchlistGetter()
    else:
        raise ValueError("URL seems not to be a valid IMDb link.")

    elements = wp.get_media_from_url(watchlist_url)

    res = check_availability(elements, location_code, progress_tracker)

    return res


def check_top_250_movies(location_code: str, progress_tracker=None) -> Results:

    elements = get_top_250()

    res = check_availability(elements, location_code, progress_tracker)
    return res
