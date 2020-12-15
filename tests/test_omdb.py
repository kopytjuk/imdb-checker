from logic.omdb import get_media_info, get_media_info_by_name_and_year, MediaInfo

def test_get_media_info():

    imdb_id = "tt0083866"

    expected_info = MediaInfo(
        name="E.T. the Extra-Terrestrial",
        description="A troubled child summons the courage to help a friendly alien escape Earth and return to his home world.",
        poster="https://m.media-amazon.com/images/M/MV5BMTQ2ODFlMDAtNzdhOC00ZDYzLWE3YTMtNDU4ZGFmZmJmYTczXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg"
    )

    info = get_media_info(imdb_id)

    assert info == expected_info


def test_get_media_info_by_name_and_year():

    name = "Around the World in 80 Days"
    year = 1956

    expected_info = MediaInfo(
        name="Around the World in 80 Days",
        description="A Victorian Englishman bets that with the new steamships and railways he can circumnavigate the globe in eighty days.",
        poster="https://m.media-amazon.com/images/M/MV5BNjRhNjVlYTgtODZiOS00OTVhLWE4ZTItZjc3MTFiYWY1YjI5L2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg"
    )

    info = get_media_info_by_name_and_year(name, year)

    assert info == expected_info

