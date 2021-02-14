"""Functions to check the availability of a list of MediaElements"""
from typing import List, Union

from .datatypes import MediaElement, ResultElement
from .justwatch import availability_table, STREAM_PROVIDERS_NAMES
from .omdb import get_media_info
from .config import SUPPORTED_LOCATION_CODES


def check_availability(elements: List[MediaElement], location_code: str, progress_tracker=None)\
        -> List[ResultElement]:

    validate_location_code(location_code)

    N = len(elements)

    if progress_tracker:
        progress_tracker.info(
            "Found %d elements. Checking takes up to %d seconds." % (N, int(N*0.2)))

    avail_df = availability_table(elements, location_code, progress_tracker)

    avail_list = avail_df.to_dict(orient="records")

    if progress_tracker:
        progress_tracker.info("Retrieving posters and descriptions...")

    movie_info_list = [get_media_info(e.imdb_id) for e in elements]

    if progress_tracker:
        progress_tracker.info("Almost done...")

    result = [finalize_result(we.name, we.year, avail, movie_info) for
              we, avail, movie_info in zip(elements, avail_list, movie_info_list)]

    return result


def finalize_result(name: str, year: Union[int, None], availability: dict, movie_info: dict)\
        -> ResultElement:

    result = {
        "name": name,
        "year": year if year else "n/a",
        "availability": {provider: availability[provider] for provider in STREAM_PROVIDERS_NAMES},
        "poster": movie_info.poster if movie_info else "",
        "description": movie_info.description if movie_info else "n/a",
        "num_available": availability["num_available"]
    }
    return result


def validate_location_code(location_code: str):
    if location_code in SUPPORTED_LOCATION_CODES:
        return
    else:
        raise ValueError("Location '%s' is not supported!" % location_code)
