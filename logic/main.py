"""Main entry point for each celery worker (process). Each function outputs a list of
datatypes.Results object
"""
from typing import List

from .datatypes import ResultElement
from .imdb_utils import get_top_250, get_media_from_watchlist_url
from .availability import check_availability


def check_imdb_user_watchlist(watchlist_url: str, location_code: str,
                              progress_tracker=None) -> List[ResultElement]:

    if "www.imdb.com" in watchlist_url:
        elements = get_media_from_watchlist_url(watchlist_url)
    else:
        raise ValueError("URL seems not to be a valid IMDb link.")

    res = check_availability(elements, location_code, progress_tracker)

    return res


def check_imdb_top_250_movies(location_code: str, progress_tracker=None) -> List[ResultElement]:

    elements = get_top_250()

    res = check_availability(elements, location_code, progress_tracker)
    return res
