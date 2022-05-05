import itertools
import timeit
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


def test_filter_basic():
    css = """
    .test1, .test3 {
        color: red;
    }
    .test2 {
        color: blue;
    }
    """

    html = """
    <a class="test1 some-other-cls">test</a>
    """

    res_css = filter_css(css, html)
    assert "test1" in res_css
    assert "test2" not in res_css


def test_filter_bootstrap_basic(bootstrap_css):
    html = """
    <div class="col"><div class="row"><p class="lead"></p></div></div>
    """

    res_css = filter_css(bootstrap_css, html)
    assert "col" in res_css
    assert "row" in res_css
    assert "lead" in res_css


def test_soup_parsers(bootstrap_css, basic_boostrap):
    def time(function):
        seconds = timeit.Timer(function).repeat(3, 5)
        miliseconds = int((min(seconds) / 5) * 1000)
        return miliseconds

    results = {}
    times = {}
    for parser in ("lxml", "html.parser", "html5lib"):
        results[parser] = filter_css(bootstrap_css, basic_boostrap, soup_features=parser)
        times[parser] = time(lambda: filter_css(bootstrap_css, basic_boostrap, soup_features=parser))

    print(times)
    for one, other in itertools.combinations(results.items(), 2):
        assert one[1] == other[1]
