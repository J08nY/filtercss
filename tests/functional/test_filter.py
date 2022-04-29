from pathlib import Path
from filtercss import filter_css

import pytest


@pytest.fixture(scope="session")
def bootstrap_css():
    path = Path(__file__).parent / "data" / "bootstrap.css"
    with path.open("r") as f:
        return f.read()


@pytest.fixture(scope="session")
def bootstrap_min_css():
    path = Path(__file__).parent / "data" / "bootstrap.min.css"
    with path.open("r") as f:
        return f.read()


@pytest.fixture(scope="session")
def basic_boostrap():
    path = Path(__file__).parent / "data" / "basic_bootstrap.html"
    with path.open("r") as f:
        return f.read()


@pytest.fixture(scope="session")
def album_boostrap():
    path = Path(__file__).parent / "data" / "album_bootstrap.html"
    with path.open("r") as f:
        return f.read()


def test_filter_bootstrap(bootstrap_css, basic_boostrap, album_boostrap):
    res_basic = filter_css(bootstrap_css, basic_boostrap)
    res_album = filter_css(bootstrap_css, album_boostrap)

    assert len(res_basic) < len(bootstrap_css)
    assert len(res_album) < len(bootstrap_css)


def test_filter_bootstrap_min(bootstrap_min_css, basic_boostrap, album_boostrap):
    res_basic = filter_css(bootstrap_min_css, basic_boostrap)
    res_album = filter_css(bootstrap_min_css, album_boostrap)

    assert len(res_basic) < len(bootstrap_min_css)
    assert len(res_album) < len(bootstrap_min_css)
