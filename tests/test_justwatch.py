import time

import pytest
import pandas as pd

from logic.justwatch import get_movie_id, availability_table
from logic.datatypes import MediaElement
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
        MediaElement("John Wick", 2014, "tt2911666"),
        MediaElement("John Wick: Chapter 2", 2017, "tt4425200"),
        MediaElement("Inception", 2010, "tt1375666"),
        MediaElement("Around the World in Eighty Days", 1956, "tt0048960"),
        MediaElement("Woman Walks Ahead", 2017, "tt5436228")
    ]

    avail_df = availability_table(elements, location_code)

    assert isinstance(avail_df, pd.DataFrame)
    assert len(avail_df) == len(elements)

    print(avail_df)

    if location_code == "de_DE":

        # John Wick Chapter 2
        assert avail_df.iloc[1]["Netflix"]
        assert not avail_df.iloc[1]["Amazon"]
        assert not avail_df.iloc[1]["Disney+"]

        # Around the World in Eighty Days
        assert not avail_df.iloc[3]["Netflix"]
        assert not avail_df.iloc[3]["Amazon"]
        assert not avail_df.iloc[3]["Disney+"]

        # Woman Walks Ahead from 2017
        assert not avail_df.iloc[4]["Netflix"]
        assert not avail_df.iloc[4]["Amazon"]
        assert not avail_df.iloc[4]["Disney+"]
