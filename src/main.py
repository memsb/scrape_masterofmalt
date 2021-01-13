from src.scrape import get_latest_stock_additions, display_stock
from src.storage import has_stock_update, store_stock
import logging

logging.basicConfig(level=logging.INFO)


def main():
    stock = get_latest_stock_additions()
    display_stock(stock)
    if has_stock_update(stock):
        logging.info('Everything is up to date')
    else:
        store_stock(stock)


def lambda_handler():
    main()


if __name__ == "__main__":
    main()
