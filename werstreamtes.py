"""
curl 'https://www.werstreamt.es/suche/suggestTitle?term=John+Wick+2' \
  -H 'authority: www.werstreamt.es' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.werstreamt.es/' \
  -H 'accept-language: de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5' \
  --compressed
"""

import json
from collections import OrderedDict, namedtuple
from typing import Union, List

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

URL_TEMPLATE_SUGGESTION = "https://www.werstreamt.es/suche/suggestTitle?term={:s}"
URL_TEMPLATE_MOVIE_DETAILS = "https://www.werstreamt.es/film/details/{:s}"

STREAM_PROVIDERS = {
    "Amazon": "10",
    "Netflix": "11",
    "Disney+": "42"
}

STREAM_PROVIDERS_INV = {v: k for k, v in STREAM_PROVIDERS.items()}

AvailabilityResult = namedtuple('AvailabilityResult', ["Amazon", "Netflix"])

def prepare_movie_name_for_url(movie_name: str) -> Union[str, None]:
    return movie_name.replace(" ", "+")


def get_movie_id(movie_name: str) -> str:

    movie_name_for_url = prepare_movie_name_for_url(movie_name)

    search_url = URL_TEMPLATE_SUGGESTION.format(movie_name_for_url)
    headers = {
        "authority": "www.werstreamt.es",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "x-requested-with": "XMLHttpRequest",
        "sec-fetch-site": "same-origin",
    }

    response = requests.get(search_url, headers=headers)

    parsed_result_dict = json.loads(response.text, object_pairs_hook=OrderedDict)

    suggested_movies = list(parsed_result_dict.keys())

    # API always returns something, >2 is relevant
    if len(suggested_movies) < 2:
        return None

    movie_id = list(suggested_movies)[0]

    # cut the 'id-' substring
    movie_id = movie_id.replace("id-", "")

    return movie_id


def check_flatrate_available(provider_div: "bs4.element.Tag") -> bool:
    check = provider_div.find("i", class_='fi-check')
    return bool(check)


def get_provider(provider_div: "bs4.element.Tag") -> str:
    data = json.loads(provider_div.attrs['data-options'])
    return STREAM_PROVIDERS_INV[data["StreamProviderID"]]


def check_availability(movie_id: str) -> dict:

    details_url = URL_TEMPLATE_MOVIE_DETAILS.format(movie_id)
    response = requests.get(details_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    provider_divs = soup.find_all('div', class_="provider")

    def filter_supported_providers(div):
        data = json.loads(div.attrs['data-options'])
        if data["StreamProviderID"] in STREAM_PROVIDERS.values():
            return True
        else:
            return False

    supported_divs = list(filter(filter_supported_providers, provider_divs))

    result = dict()
    for prov_div in supported_divs:
        prov_name = get_provider(prov_div)
        is_available = check_flatrate_available(prov_div)
        result[prov_name] = is_available

    return result


def availability(movie_name: str) -> dict:

    movie_id = get_movie_id(movie_name)

    result = STREAM_PROVIDERS.copy()

    # prefill
    for prov in result.keys():
        result[prov] = False
        
    if not movie_id:
        return result
    else:
        avail = check_availability(movie_id)
        for provider, is_available in avail.items():
            result[provider] = is_available
        return result


def availability_table(movies: List[str]) -> pd.DataFrame:

    dict_list = list()
    for movie in tqdm(movies):
        avail: dict = availability(movie)
        avail["Name"] = movie
        dict_list.append(avail)

    df = pd.DataFrame(dict_list)
    df = df.set_index("Name")
    return df
