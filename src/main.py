from pathlib import Path
from typing_extensions import Annotated

from loguru import logger
import typer
from pydantic_yaml import parse_yaml_raw_as
from .reverb_transaction import record_transactions, TransactionConfig
from .listing import get_listing, GuitarWebPage

app = typer.Typer()

epiphone_urls = [
    "https://www.epiphone.com/en-US/Collection/modern-les-paul",
    "https://www.epiphone.com/en-US/Collection/original-es",
    "https://www.epiphone.com/en-US/Collection/les-paul",
]

gibson_urls = [
    "https://www.gibson.com/en-US/Collection/les-paul",
    "https://www.gibson.com/en-US/Collection/es",
]


@app.command()
def listing():
    logger.info("Starting")
    urls = epiphone_urls + gibson_urls
    listing_ = get_listing(urls)
    listing_file = Path("listing.json")
    listing_file.write_text(listing_.model_dump_json(by_alias=True, indent=4))

    logger.info("Done")


@app.command()
def guitar_details(url: str):
    logger.info("Starting")
    web_page = GuitarWebPage(url)
    details = web_page.get_guitar_details()
    listing_file = Path(f"{details.model}.json")
    listing_file.write_text(details.model_dump_json(by_alias=True, indent=4))

    logger.info("Done")


@app.command()
def transactions(config_file: Annotated[typer.FileText, typer.Option()]):
    logger.info("Starting")
    config = parse_yaml_raw_as(TransactionConfig, config_file)
    record_transactions(config.urls)
    logger.info("Done")


if __name__ == "__main__":
    transactions()
