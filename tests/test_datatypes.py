from logic.datatypes import MediaList, MediaElement
from pathlib import Path


def test_medialist_write_read(tmp_path: Path):

    elements = [
        MediaElement("A", 2000, "tt0001"),
        MediaElement("B", 2000, "tt0002"),
        MediaElement("C", 2001, "tt0003"),
    ]

    medialist = MediaList("Sample list", elements)

    path = tmp_path / "sample.csv"

    medialist.to_csv(str(path))

    assert path.exists()

    medialist = MediaList.from_csv("Sample list", path)

    assert len(medialist) == len(elements)
