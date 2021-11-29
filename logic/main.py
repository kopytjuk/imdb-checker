"""Main entry point for each celery worker (process). Each function outputs a list of
datatypes.Results object
"""
from typing import List
import pathlib

from .datatypes import ResultElement, MediaList
from .imdb_utils import get_media_from_watchlist_url
from .availability import check_availability


def check_imdb_user_watchlist(watchlist_url: str, location_code: str,
                              progress_tracker=None) -> List[ResultElement]:

    if "www.imdb.com" in watchlist_url:
        medialist = get_media_from_watchlist_url(watchlist_url)
    else:
        raise ValueError("URL seems not to be a valid IMDb link.")

    res = check_availability(medialist, location_code, progress_tracker)

    return res


def check_medialist(name: str, location_code: str, progress_tracker=None) -> List[ResultElement]:

    medialist_path = pathlib.Path(".\medialists") / ("%s.csv" % name)

    medialist = MediaList.from_csv(name, str(medialist_path))
    res = check_availability(medialist, location_code, progress_tracker)
    return res
