import pytest
import json
from pathlib import Path
from src.listing import ListingWebPage, GuitarWebPage
from src.listing_models import GuitarDetails

current_folder = Path(__file__).parent


@pytest.fixture(scope="module")
def vcr_config():
    # https://pytest-vcr.readthedocs.io/en/latest/
    # https://vcrpy.readthedocs.io/en/latest/configuration.html
    # selenium keeps on changing the port number under the hood
    return {"match_on": ["method", "scheme", "host", "path", "query"]}


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "url,expected",
    [
        pytest.param(
            "https://www.epiphone.com/en-US/Collection/modern-les-paul",
            30,
            id="modern-les-paul",
        ),
        pytest.param(
            "https://www.epiphone.com/en-US/Collection/original-es",
            16,
            id="original-es",
        ),
        pytest.param(
            "https://www.epiphone.com/en-US/Collection/les-paul", 58, id="les-paul"
        ),
        pytest.param(
            "https://www.gibson.com/en-US/Collection/les-paul",
            144,
            id="gibson-les-paul",
        ),
        pytest.param("https://www.gibson.com/en-US/Collection/es", 62, id="gibson-es"),
    ],
)
def test_ListingWebPage_get_elements(url: str, expected: int):
    page = ListingWebPage(url)
    page.sleep = 0
    res = page.get_elements()
    assert len(res) == expected


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "url,expected_json",
    [
        pytest.param(
            "https://www.epiphone.com/en-US/Electric-Guitar/EPIQM1648/Cherry",
            "./data/bb-king-lucille-cherry.json",
            id="BB King Lucille Cherry",
        ),
        pytest.param(
            "https://www.gibson.com/en-US/Electric-Guitar/Kirk-Hammett-Greeny-Custom/Greeny-Burst",
            "./data/gibson-custom-shop-greeny.json",
            id="Gibson Custom shop Greeny",
        ),
    ],
)
def test_GuitarWebPage_get_guitar_details(url: str, expected_json: str):
    file_json = current_folder / Path(expected_json)
    data_json = json.loads(file_json.read_text())
    expected = GuitarDetails(**data_json)
    page = GuitarWebPage(url)
    page.sleep = 0
    res = page.get_guitar_details()
    assert res == expected


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "url,expected",
    [
        pytest.param(
            "https://www.epiphone.com/en-US/Electric-Guitar/EPIQM1648/Cherry",
            38,
            id="BB King Lucille Cherry",
        ),
        pytest.param(
            "https://www.gibson.com/en-US/Electric-Guitar/Kirk-Hammett-Greeny-Custom/Greeny-Burst",
            38,
            id="Gibson Custom shop Greeny",
        ),
    ],
)
def test_GuitarWebPage_get_all_h6(url: str, expected: int):
    page = GuitarWebPage(url)
    page.sleep = 0
    res = page.get_all_h6(page.get_master_content())
    assert len(res) == expected


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "url",
    [
        pytest.param(
            "https://www.epiphone.com/en-US/Electric-Guitar/EPIQM1648/Cherry",
            id="BB King Lucille Cherry",
        ),
        pytest.param(
            "https://www.gibson.com/en-US/Electric-Guitar/Kirk-Hammett-Greeny-Custom/Greeny-Burst",
            id="Gibson Custom shop Greeny",
        ),
    ],
)
def test_GuitarWebPage_get_master_content(url: str):
    page = GuitarWebPage(url)
    page.sleep = 0
    assert page.get_master_content()


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "url,expected",
    [
        pytest.param(
            "https://www.epiphone.com/en-US/Electric-Guitar/EPIQM1648/Cherry",
            "B.B. King Lucille, Exclusive",
            id="BB King Lucille Cherry",
        ),
        pytest.param(
            "https://www.gibson.com/en-US/Electric-Guitar/Kirk-Hammett-Greeny-Custom/Greeny-Burst",
            'Kirk Hammett "Greeny" 1959 Les Paul Standard',
            id="Gibson Custom shop Greeny",
        ),
    ],
)
def test_GuitarWebPage_get_model(url: str, expected: str):
    page = GuitarWebPage(url)
    page.sleep = 0
    assert page.get_model() == expected


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "url,expected",
    [
        pytest.param(
            "https://www.epiphone.com/en-US/Electric-Guitar/EPIQM1648/Cherry",
            "Cherry",
            id="BB King Lucille Cherry",
        ),
        pytest.param(
            "https://www.gibson.com/en-US/Electric-Guitar/Kirk-Hammett-Greeny-Custom/Greeny-Burst",
            "Greeny Burst",
            id="Gibson Custom shop Greeny",
        ),
        pytest.param(
            "https://www.gibson.com/en-US/Electric-Guitar/Les-Paul-Supreme/Fireburst",
            "Fireburst;Dark Wine Red;Translucent Ebony Burst",
            id="Gibson Les Paul Supreme",
        ),
    ],
)
def test_GuitarWebPage_get_finishes(url: str, expected: str):
    page = GuitarWebPage(url)
    page.sleep = 0
    assert page.get_finishes() == expected
