import json
from pathlib import Path
from typing_extensions import Annotated

from loguru import logger
import typer
from pydantic_yaml import parse_yaml_raw_as
from .reverb_transaction import record_transactions, TransactionConfig
from .listing import get_listing

app = typer.Typer()

epiphone_urls = [
    # "https://www.epiphone.com/en-US/Collection/modern-les-paul",
    "https://www.epiphone.com/en-US/Collection/original-es",
    # "https://www.epiphone.com/en-US/Collection/les-paul",
]

gibson_urls = [
    # "https://www.gibson.com/en-US/Collection/les-paul",
    # "https://www.gibson.com/en-US/Collection/es",
]


@app.command()
def listing():
    logger.info("Starting")
    urls = epiphone_urls + gibson_urls
    listing_ = get_listing(urls)
    # json_listing = json.dumps(listing_.model_dump(), indent=4)
    listing_file = Path("listing.json")
    listing_file.write_text(listing_.model_dump_json(indent=4))

    logger.info("Done")


@app.command()
def transactions(config_file: Annotated[typer.FileText, typer.Option()]):
    logger.info("Starting")
    config = parse_yaml_raw_as(TransactionConfig, config_file)
    record_transactions(config.urls)
    logger.info("Done")


if __name__ == "__main__":
    transactions()
