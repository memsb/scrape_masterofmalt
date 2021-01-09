import unittest
from lib import scrape
import responses
import requests
from decimal import *


class TestScrape(unittest.TestCase):

    @responses.activate
    def test_simple(self):
        responses.add(responses.GET, 'http://twitter.com/api/1/foobar',
                      json={'error': 'not found'}, status=404)

        resp = requests.get('http://twitter.com/api/1/foobar')

        self.assertEqual(resp.json(), {"error": "not found"})

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, 'http://twitter.com/api/1/foobar')
        self.assertEqual(responses.calls[0].response.text, '{"error": "not found"}')

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
