from collections import namedtuple
import requests
from urllib.parse import quote_plus
from typing import Union, List

from .config import OMDB_API_KEY


MediaInfo = namedtuple("MediaInfo", ["name", "description", "poster"])


def get_media_info(imdb_id: str) -> MediaInfo:

    omdb_url = "http://www.omdbapi.com/?apikey=%s&i=%s" % (OMDB_API_KEY, imdb_id)

    response = requests.get(omdb_url)

    response_dict = response.json()

    try:
        m = MediaInfo(response_dict["Title"], response_dict["Plot"], response_dict["Poster"])
    except KeyError:
        return None

    return m


def get_media_info_by_name_and_year(name: str, year: Union[int, None]) -> Union[MediaInfo, None]:

    url = "http://www.omdbapi.com/?apikey=%s&t=%s" % (OMDB_API_KEY, quote_plus(name))

    if year:
        url += "&y=%d" % year

    response = requests.get(url)

    response_dict = response.json()

    try:
        m = MediaInfo(response_dict["Title"], response_dict["Plot"], response_dict["Poster"])
    except KeyError:
        return None
    return m


def get_media_info_batch(imdb_ids: List[str]):
    pass
