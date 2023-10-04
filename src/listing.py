from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import List, Optional, Set

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from loguru import logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait

from src.listing_models import Listing, GuitarDetails, Brand


@dataclass
class ListingWebPage:
    """Represents the web page where the guitars are listed."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.base_url = self.url.split("/en-US/")[0]
        self.brand = Brand.gibson if "gibson.com" in self.url else Brand.epiphone
        self.__content: Optional[BeautifulSoup] = None

    @property
    def content(self) -> BeautifulSoup:
        if not self.__content:
            with content(self.url, max_wait_time=3) as page:
                time.sleep(1)
                self.__content = BeautifulSoup(page.page_source, features="html.parser")

        return self.__content

    def get_elements(self) -> ResultSet:
        return self.content.find_all(class_="cmp-products-grid-korina__item__url")

    def get_unique_urls(self, elements: List[ResultSet]) -> Set[str]:
        return {"".join([self.base_url, element.get("href")]) for element in elements}


def get_listing(urls: List[str]) -> Listing:
    listing = Listing(guitars=[])
    for url in urls:
        listing.guitars.extend(get_listing_from_page(url))
    return listing


def get_listing_from_page(url: str) -> list[GuitarDetails]:
    listing_web_page = ListingWebPage(url)
    logger.info(f"Listing guitars from {listing_web_page.brand.value}: {url}")
    elements = listing_web_page.get_elements()
    unique_links = listing_web_page.get_unique_urls(elements)
    listing = []
    for i, link in enumerate(unique_links):
        logger.info(f" - {i + 1}/{len(unique_links)}: {link}")
        try:
            listing.append(get_content(listing_web_page.brand, link))
        except AttributeError as e:
            logger.warning(f"skipping {link}: {e}")

    return listing


def get_content(brand: Brand, link: str) -> GuitarDetails:
    with content(link) as guitar:
        soup = BeautifulSoup(guitar.page_source, features="html.parser")
        details = GuitarDetails.get(soup, brand, link)
        return details


@contextmanager
def content(url: str, max_wait_time: int = 1) -> webdriver.Firefox:
    options = FirefoxOptions()
    options.add_argument("--headless")
    # Set up the eebDriver (make sure to provide the path to the GeckoDriver executable)
    driver = webdriver.Firefox(options=options)

    # Open the page
    driver.get(url)

    # Wait for the page to fully load
    WebDriverWait(driver, max_wait_time)

    yield driver
    driver.quit()
