import json
from pathlib import Path

from loguru import logger
import typer

from .reverb_transaction import get_transactions
from .listing import get_listing

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

reverb_guitar_urls = [
    "https://reverb.com/ca/p/epiphone-bb-king-lucille",
    "https://reverb.com/ca/p/gibson-kirk-hammett-greeny-les-paul-standard",
    "https://reverb.com/ca/p/epiphone-joe-bonamassa-signature-lazarus-59-les-paul-standard",
    "https://reverb.com/ca/p/epiphone-59-les-paul-standard-outfit",
    "https://reverb.com/ca/p/gibson-custom-shop-murphy-lab-59-les-paul-standard-reissue-ultra-light-aged",
    "https://reverb.com/ca/p/epiphone-joe-bonamassa-black-beauty-les-paul-custom-outfit",
    "https://reverb.com/ca/p/epiphone-joe-bonamassa-signature-les-paul-standard",
]


@app.command()
def listing():
    logger.info("Starting")
    urls = epiphone_urls + gibson_urls
    listing_ = get_listing(urls)
    json_listing = json.dumps(listing_, indent=4)
    listing_file = Path("listing.json")
    listing_file.write_text(json_listing)

    logger.info("Done")


@app.command()
def transactions():
    logger.info("Starting")
    listing_ = get_transactions(reverb_guitar_urls)
    json_listing = json.dumps(listing_, indent=4)
    listing_file = Path("prices.json")
    listing_file.write_text(json_listing)
    logger.info("Done")


if __name__ == '__main__':
    transactions()
