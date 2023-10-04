import pytest
from src.listing import ListingWebPage


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
    res = ListingWebPage(url).get_elements()
    assert len(res) == expected
