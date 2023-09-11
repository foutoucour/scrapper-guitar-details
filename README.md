# scrapper-guitar-details
a series of script to scrap details from gibson.com, epiphone.com and reverb.com


# How to

First, run `poetry install`

## reverb.com transactions:

1. update the `reverb_guitar_urls` in `main.py` with the url of the guitar you want to get the transaction history from
2. run `poetry run scrapper transactions`
3. PS: the script will wait for you to click on the `Next transactions` button.
3. the content is saved in `reverb_transaction.json`

## TODO:
* Add the automatic click to the `Next transactions`
* move the urls in a config file
* add option to mention a specific url
* add option to mention the config file


## guitar listing from Gibson.con and Epiphone.com

1. update the list `epiphone_urls` and `gibson_urls` in `main.py`
2. run `poetry run scrapper listing`
3. the results are saved in `content.json`

## TODO:
* move the urls in a config file
* add option to mention a specific url
* add option to mention the config file


# TODO:
* add CI and tests
