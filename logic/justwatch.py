import json
from urllib.parse import quote_plus
from typing import List, Union, Optional
from multiprocessing.pool import ThreadPool

import pandas as pd
from pydantic import BaseModel, ValidationError

from .watchlist_provider import WatchlistElement
from .web_utils import retry_session
from .config import memory

STREAM_PROVIDERS = {
    "Amazon": 9,
    "Netflix": 8,
    "Disney+": 337
}

STREAM_PROVIDERS_NAMES = list(STREAM_PROVIDERS.keys())

STREAM_PROVIDERS_INV = {v: k for k, v in STREAM_PROVIDERS.items()}
class Offer(BaseModel):
    monetization_type: str
    provider_id: int
    urls: dict

class ExternalId(BaseModel):
    provider: str
    external_id: str

class MediaEntity(BaseModel):
    jw_entity_id: str
    id: int
    object_type: str
    original_title: str
    offers: Optional[List[Offer]]
    external_ids: List[ExternalId]
    runtime: Optional[int]
    full_path: Optional[str]
    title: str
    original_title: str
    original_release_year: int


def is_same_imdb_id(entity: MediaEntity, imdb_id: str) -> False:

    for ext in entity.external_ids:
        if ext.provider == "imdb":
            return ext.external_id == imdb_id
    return False

session = retry_session(3)


def get_movie_id(movie_name: str, year: Union[int, None], location: str = "de_DE") -> Union[str, None]:

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

    first_suggested_item = suggested_items[0]

    movie_id = str(first_suggested_item["id"])

    return movie_id


def check_offers(offers: List[Offer]) -> dict:

    result = STREAM_PROVIDERS.copy()

    # prefill all providers to False
    for prov in result.keys():
        result[prov] = False

    if len(offers) < 1:
        return result

    for offer in offers:
        provider = offer.provider_id
        monetization_type = offer.monetization_type

        if (provider in STREAM_PROVIDERS.values()) and monetization_type == "flatrate":
            result[STREAM_PROVIDERS_INV[provider]] = True

    return result


@memory.cache()
def availability(movie_name: str, year: Union[int, None], imdb_id: str, location_code: str) -> dict:

    movie_id = get_movie_id(movie_name, year, location_code)

    result = STREAM_PROVIDERS.copy()

    # prefill
    for prov in result.keys():
        result[prov] = False

    if not movie_id:
        return result
    else:
        entity = get_entity_by_id(movie_id, location_code)

        if not entity:
            return result

        if not is_same_imdb_id(entity, imdb_id):
            return result

        if year:
            if entity.original_release_year != year:
                return result

        if not entity.offers:
            return result

        avail = check_offers(entity.offers)
        for provider, is_available in avail.items():
            result[provider] = is_available
        return result


def availability_table(watchlist_elements: List[WatchlistElement], location_code: str,
                       progress_tracker=None) -> pd.DataFrame:

    pool = ThreadPool(4)

    def check_avail(movie: str, year: Union[int, None], imdb_id: str):

        avail: dict = availability(movie, year, imdb_id, location_code)
        avail["Name"] = movie
        
        return avail

    avail_list = pool.starmap(
        check_avail, [(e.name, e.year, e.imdb_id) for e in watchlist_elements])

    df = pd.DataFrame(avail_list)
    df = df.set_index("Name")

    df["num_available"] = df[STREAM_PROVIDERS_NAMES].sum(axis=1)

    return df


def get_entity_by_id(movie_id: str, location_code: str) -> Union[MediaEntity, None]:

    details_base_url = "https://apis.justwatch.com/content/titles/movie/{:s}/locale/{:s}"
    details_url = details_base_url.format(movie_id, location_code)

    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = session.get(details_url, headers=headers)
    response_dict = response.json()
    try:
        entity = MediaEntity(**response_dict)
    except ValidationError as ex:
        return None

    return entity
