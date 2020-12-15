import json
from urllib.parse import quote_plus
from typing import List, Union
from multiprocessing.pool import ThreadPool

import pandas as pd

from .watchlist_provider import WatchlistElement
from .web_utils import retry_session

STREAM_PROVIDERS = {
    "Amazon": 9,
    "Netflix": 8,
    "Disney+": 337
}

STREAM_PROVIDERS_INV = {v: k for k, v in STREAM_PROVIDERS.items()}

session = retry_session(3)


def get_movie_id(movie_name: str, year: Union[int, None], location: str = "de_DE") -> str:

    search_url_base = "https://apis.justwatch.com/content/titles/{:s}/popular?body={:s}"

    query_dict = {"query": movie_name,
                  "content_types": ["show", "movie"]}

    if year:
        query_dict["release_year_from"] = year
        query_dict["release_year_until"] = year

    query_str = quote_plus(json.dumps(query_dict))

    search_url = search_url_base.format(location, query_str)

    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = session.get(search_url, headers=headers)

    try:
        resp_json = response.json()
    except json.decoder.JSONDecodeError:
        return None

    if not "items" in resp_json:
        return None

    suggested_items = resp_json["items"]

    if len(suggested_items) < 1:
        return None

    movie_id = str(suggested_items[0]["id"])

    return movie_id


def check_offers(offers: List[dict]) -> dict:

    result = STREAM_PROVIDERS.copy()

    # prefill all providers to False
    for prov in result.keys():
        result[prov] = False

    if len(offers) < 1:
        return result

    for offer in offers:

        provider = offer["provider_id"]
        monetization_type = offer["monetization_type"]

        if (provider in STREAM_PROVIDERS.values()) and monetization_type == "flatrate":
            result[STREAM_PROVIDERS_INV[provider]] = True

    return result


def check_availability(movie_id: str, location_code: str) -> dict:

    details_base_url = "https://apis.justwatch.com/content/titles/movie/{:s}/locale/{:s}?language=de"
    details_url = details_base_url.format(movie_id, location_code)

    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = session.get(details_url, headers=headers)

    try:
        resp_json = response.json()
        result = check_offers(resp_json["offers"])
    except:
        return dict()

    return result


def availability(movie_name: str, year: Union[int, None], location_code: str) -> dict:

    movie_id = get_movie_id(movie_name, year)

    result = STREAM_PROVIDERS.copy()

    # prefill
    for prov in result.keys():
        result[prov] = False

    if not movie_id:
        return result
    else:
        avail = check_availability(movie_id, location_code)
        for provider, is_available in avail.items():
            result[provider] = is_available
        return result


def availability_table(watchlist_elements: List[WatchlistElement], location_code: str,
                       progress_tracker=None) -> pd.DataFrame:

    pool = ThreadPool(4)

    def check_avail(movie: str, year: Union[int, None]):
        avail: dict = availability(movie, year, location_code)
        avail["Name"] = movie
        return avail

    avail_list = pool.starmap(
        check_avail, [(e.name, e.year) for e in watchlist_elements])

    df = pd.DataFrame(avail_list)
    df = df.set_index("Name")

    return df
