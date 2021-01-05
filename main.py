from scrape import get_latest_stock_additions, display_stock
from storage import has_stock_update, store_stock


def main():
    stock = get_latest_stock_additions()
    display_stock(stock)
    if has_stock_update(stock):
        print('Everything is up to date')
    else:
        store_stock(stock)


def lambda_handler(event, context):
    main()


if __name__ == "__main__":
    main()
