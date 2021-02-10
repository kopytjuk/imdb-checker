import time

import pytest
import pandas as pd

from logic.justwatch import get_movie_id, availability_table
from logic.watchlist_provider import WatchlistElement
from logic.config import SUPPORTED_LOCATION_CODES


@pytest.mark.parametrize("location_code", SUPPORTED_LOCATION_CODES)
def test_get_movie_id(location_code: str):

    test_movie = "John Wick: Chapter 2"
    year = 2017

    movie_id = get_movie_id(test_movie, year, location_code)

    assert movie_id == "233164"

    time.sleep(0.5)


@pytest.mark.parametrize("location_code", SUPPORTED_LOCATION_CODES)
def test_availability_table(location_code: str):

    elements = [
        WatchlistElement("John Wick", 2014, "tt2911666"),
        WatchlistElement("John Wick: Chapter 2", 2017, "tt4425200"),
        WatchlistElement("Inception", 2010, "tt1375666"),
        WatchlistElement("Around the World in Eighty Days", 1956, "tt0048960"),
        WatchlistElement("Woman Walks Ahead", 2017, "tt5436228")
    ]

    avail_df = availability_table(elements, location_code)

    assert isinstance(avail_df, pd.DataFrame)
    assert len(avail_df) == len(elements)

    print(avail_df)

    if location_code == "de_DE":
        
        # John Wick Chapter 2
        assert avail_df.iloc[1]["Netflix"] == True
        assert avail_df.iloc[1]["Amazon"] == False
        assert avail_df.iloc[1]["Disney+"] == False

        # Around the World in Eighty Days
        assert avail_df.iloc[3]["Netflix"] == False
        assert avail_df.iloc[3]["Amazon"] == False
        assert avail_df.iloc[3]["Disney+"] == False

        # Woman Walks Ahead from 2017
        assert avail_df.iloc[4]["Netflix"] == False
        assert avail_df.iloc[4]["Amazon"] == False
        assert avail_df.iloc[4]["Disney+"] == False
