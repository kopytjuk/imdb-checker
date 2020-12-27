from typing import Union, List

from .justwatch import availability_table
from .imdb import IMDbWatchlistGetter
from .omdb import get_media_info, MediaInfo

from .watchlist_provider import WatchlistError
from .config import SUPPORTED_LOCATION_CODES


def finalize_result(name: str, year: Union[int, None], availability: dict, movie_info: Union[MediaInfo, None]):

    result = {
        "name": name,
        "year": year if year else "n/a",
        "availability": availability,
        "poster": movie_info.poster if movie_info else "",
        "description": movie_info.description if movie_info else "n/a"
    }
    return result


def validate_location_code(location_code: str):
    if location_code in SUPPORTED_LOCATION_CODES:
        return
    else:
        raise ValueError("Location '%s' is not supported!" % location_code)


def check(watchlist_url: str, location_code: str, progress_tracker=None) -> List[dict]:

    if "www.imdb.com" in watchlist_url:
        wp = IMDbWatchlistGetter()
    else:
        raise ValueError("URL seems not to be a valid IMDb link.")

    validate_location_code(location_code)

    watchlist_elements = wp.get_media_from_url(watchlist_url)

    N = len(watchlist_elements)

    if progress_tracker:
        progress_tracker.info("Found %d watchlist elements. Checking takes up to %d seconds." % (N, int(N*0.2)))

    avail_df = availability_table(watchlist_elements, location_code, progress_tracker)

    avail_list = avail_df.to_dict(orient="records")

    if progress_tracker:
        progress_tracker.info("Retrieving posters and descriptions...")

    movie_info_list = [get_media_info(e.imdb_id) \
         for e in watchlist_elements]

    if progress_tracker:
        progress_tracker.info("Almost done...")
    
    result = [finalize_result(we.name, we.year, avail, movie_info)\
        for we, avail, movie_info in zip(watchlist_elements, avail_list, movie_info_list)]

    return result
