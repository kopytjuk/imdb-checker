"""Main entry point for each celery worker (process). Each function outputs a list of 
datatypes.Results object
"""

from .datatypes import Results
from .watchlist_checker import check, finalize_result
from .imdb_provider import get_top_250
from .justwatch import availability_table


def check_imdb_user_watchlist(watchlist_url: str, location_code: str,
                              progress_tracker=None) -> Results:
    return check(watchlist_url, location_code, progress_tracker)


def check_top_250_movies(location_code: str, progress_tracker=None) -> Results:

    watchlist_elements = get_top_250()

    N = len(watchlist_elements)

    if progress_tracker:
        progress_tracker.info(
            "Found %d watchlist elements. Checking takes up to %d seconds."
            % (N, int(N*0.2)))

    avail_df = availability_table(
        watchlist_elements, location_code, progress_tracker)

    avail_list = avail_df.to_dict(orient="records")

    if progress_tracker:
        progress_tracker.info("Retrieving posters and descriptions...")

    movie_info_list = [get_media_info(e.imdb_id)
                       for e in watchlist_elements]

    if progress_tracker:
        progress_tracker.info("Almost done...")

    result = [finalize_result(we.name, we.year, avail, movie_info)
              for we, avail, movie_info in zip(watchlist_elements, avail_list, movie_info_list)]

    return result
