import unittest
import lib.scrape as scrape
import responses
from decimal import *


class TestScrape(unittest.TestCase):

    @responses.activate
    def test_get_stock(self):
        with open('tests/snapshots/mom_new_stock.html', 'r') as reader:
            responses.add(responses.GET, 'https://www.masterofmalt.com/new-arrivals/whisky-new-arrivals/',
                          body=reader.read(), status=200)

            stock = scrape.get_latest_stock_additions()
            self.assertEqual('08-01-2021', stock['date'])
            self.assertEqual(1, len(stock['whiskies']))

    @responses.activate
    def test_get_stock_with_auctions(self):
        with open('tests/snapshots/new_stock_with_auctions.html', 'r') as reader:
            responses.add(responses.GET, 'https://www.masterofmalt.com/new-arrivals/whisky-new-arrivals/',
                          body=reader.read(), status=200)

            stock = scrape.get_latest_stock_additions()
            self.assertEqual('07-01-2021', stock['date'])
            self.assertEqual(6, len(stock['whiskies']))

    def test_release_date_extraction(self):
        self.assertEqual(scrape.get_release_date("1st January 2020"), "01-01-2020")
        self.assertEqual(scrape.get_release_date("2nd January 2020"), "02-01-2020")
        self.assertEqual(scrape.get_release_date("3rd January 2020"), "03-01-2020")
        self.assertEqual(scrape.get_release_date("4th July 2021"), "04-07-2021")

    def test_price_extraction(self):
        self.assertEqual(scrape.format_price("£9.99"), Decimal("9.99"))
        self.assertEqual(scrape.format_price("9.99"), Decimal("9.99"))
        self.assertEqual(scrape.format_price("£99.99"), Decimal("99.99"))
        self.assertEqual(scrape.format_price("£99"), Decimal("99.00"))


if __name__ == '__main__':
    unittest.main()
