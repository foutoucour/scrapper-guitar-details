import time
from contextlib import contextmanager
from enum import Enum
from typing import List, Dict

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from loguru import logger

from selenium.webdriver.common.by import By


def get_listing(urls: List[str]) -> List[Dict]:
    full = []
    for url in urls:
        base_url = url.split("/en-US/")[0]
        brand = Brand.gibson if "gibson.com" in url else Brand.epiphone
        logger.info(f"Listing guitars from {brand.value}: {url}")
        with content(url, max_wait_time=3) as listing:
            time.sleep(1)
            soup = BeautifulSoup(listing.page_source, features="html.parser")
            elements = soup.find_all(class_="cmp-products-grid-korina__item__url")
            unique_links = {"".join([base_url, element.get("href")]) for element in elements}
        for i, link in enumerate(unique_links):
            logger.info(f" - {i + 1}/{len(unique_links)}: {link}")
            try:
                full.append(get_content(brand, link))
            except AttributeError as e:
                logger.warning(f"skipping {link}: {e}")
    return full


class Brand(Enum):
    gibson = "Gibson"
    epiphone = "Epiphone"


def get_content(brand: Brand, link: str) -> dict:
    with content(link) as guitar:
        soup = BeautifulSoup(guitar.page_source, features="html.parser")
        master = soup.find("div", id="master-product-tab-content")
        h6 = master.find_all("h6")
        details = {
            h.getText(): h.find_next("p").getText()
            for h in h6
        }
        details["model"] = soup.find("h2").getText()

        if brand == Brand.gibson:
            finishes = [
                finish.get('aria-label')
                for finish in soup.find_all("a", class_="singleFinish")
            ]
        else:
            finishes = [
                finish.get('aria-label')
                for finish in soup.find_all("label", class_="rs-finish-button")
            ]

        details["finishes"] = ";".join(finishes)
        details["brand"] = brand.value
        details["url"] = link
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
