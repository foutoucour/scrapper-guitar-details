from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import List, Optional, Set

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from loguru import logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait

from src.listing_models import Listing, GuitarDetails, Brand


@dataclass
class ListingWebPage:
    """Represents the web page where the guitars are listed."""

    sleep = 1

    def __init__(self, url: str) -> None:
        self.url = url
        self.base_url = self.url.split("/en-US/")[0]
        self.brand = Brand.gibson if "gibson.com" in self.url else Brand.epiphone
        self.__content: Optional[BeautifulSoup] = None

    @property
    def content(self) -> BeautifulSoup:
        if not self.__content:
            with selenium_web_driver(self.url, max_wait_time=3) as driver:
                time.sleep(self.sleep)
                self.__content = BeautifulSoup(
                    driver.page_source, features="html.parser"
                )

        return self.__content

    def get_elements(self) -> ResultSet:
        return self.content.find_all(class_="cmp-products-grid-korina__item__url")

    def get_unique_urls(self, elements: List[ResultSet]) -> Set[str]:
        return {"".join([self.base_url, element.get("href")]) for element in elements}


class GuitarWebPage:
    """Represents the web page where the guitar details are listed."""

    sleep = 1

    def __init__(self, url: str) -> None:
        self.url = url
        self.brand = Brand.gibson if "gibson.com" in self.url else Brand.epiphone
        self.__content: Optional[BeautifulSoup] = None

    @property
    def content(self) -> BeautifulSoup:
        if not self.__content:
            with selenium_web_driver(self.url, max_wait_time=3) as driver:
                time.sleep(self.sleep)
                self.__content = BeautifulSoup(
                    driver.page_source, features="html.parser"
                )

        return self.__content

    def get_guitar_details(self) -> GuitarDetails:
        master = self.get_master_content()
        h6 = self.get_all_h6(master)
        raw_details = {h.getText(): h.find_next("p").getText() for h in h6}
        details = GuitarDetails(**raw_details)
        details.finishes = self.get_finishes()
        details.model = self.get_model()
        details.brand = self.brand.value
        details.url = self.url
        return details

    def get_all_h6(self, master: Tag) -> ResultSet:
        return master.find_all("h6")

    def get_master_content(self) -> Tag:
        return self.content.find("div", id="master-product-tab-content")

    def get_model(self) -> str:
        return self.content.find("h2").getText()

    def get_finishes(self) -> str:
        if self.brand == Brand.gibson:
            finishes = [
                finish.get("aria-label")
                for finish in self.content.find_all("a", class_="singleFinish")
            ]
        else:
            finishes = [
                finish.get("aria-label")
                for finish in self.content.find_all("label", class_="rs-finish-button")
            ]
        return ";".join(finishes)


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
        guitar_web_page = GuitarWebPage(link)
        try:
            listing.append(guitar_web_page.get_guitar_details())
        except AttributeError as e:
            logger.warning(f"skipping {link}: {e}")

    return listing


@contextmanager
def selenium_web_driver(url: str, max_wait_time: int = 1) -> webdriver.Firefox:
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
