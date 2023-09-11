from contextlib import contextmanager
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, Tag
from loguru import logger
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@contextmanager
def content_reverb(url: str, max_wait_time: int = 10) -> webdriver.Firefox:
    options = FirefoxOptions()
    # options.add_argument()
    # Set up the eebDriver (make sure to provide the path to the GeckoDriver executable)
    driver = webdriver.Firefox(options=options)

    # Open the page
    driver.get(url)

    # Wait for the page to fully load
    wait = WebDriverWait(driver, max_wait_time)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "v2-csp-price-guide-module-graph-and-table-container")))

    yield driver
    driver.quit()


class Transaction(BaseModel):
    model: str
    date: str
    condition: str
    price: int


def wait_for_prices(driver: webdriver.Firefox):
    wait = WebDriverWait(driver, 60, poll_frequency=0.1)
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "csp-transaction-table-container__header__loader")))
    wait.until_not(
        EC.presence_of_element_located((By.CLASS_NAME, "csp-transaction-table-container__header__loader")))


def get_transactions(urls: List[str]) -> List[dict]:
    all_transactions: List[Transaction] = []
    for url in urls:
        url = f"{url}#price-guide"
        with content_reverb(url) as driver:
            wait_for_prices(driver)
            while True:
                all_transactions.extend(get_transactions_from_table(driver, url))
                logger.info("transactions captured")
                logger.debug("wait for your click on the `Next Transactions` button.")
                wait_for_prices(driver)
                button = driver.find_element(By.XPATH, "//button[normalize-space()='Next transactions']")
                disabled = button.get_attribute("disabled")
                logger.debug(f"disabled: {disabled}")
                if disabled:
                    break

    return [sale.model_dump() for sale in all_transactions]


def get_transactions_from_table(driver: webdriver.Firefox, url: str) -> List[Transaction]:
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    master = soup.find(class_="v2-csp-price-guide-module-graph-and-table-container__transaction-table")
    tbody = master.find("tbody")
    trs = tbody.find_all("tr")
    return [get_transactions_from_tr(tr, url) for tr in trs]


def get_transactions_from_tr(tr: Tag, url: str) -> Transaction:
    date_format = "%B %d, %Y"
    tds = tr.find_all("td")
    iprice = tds[2].text.replace("$", "").replace(",", "").split(".")[0]
    sale_details = Transaction(
        model=url,
        date=datetime.strptime(tds[0].text, date_format).date().__str__(),
        condition=tds[1].text,
        price=int(iprice)
    )
    return sale_details
