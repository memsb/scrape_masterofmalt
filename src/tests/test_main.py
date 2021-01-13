import unittest
from unittest.mock import Mock
from src import main


class TestMain(unittest.TestCase):
    def test_no_new_stock(self):
        main.logging = Mock()
        main.get_latest_stock_additions = Mock()
        main.display_stock = Mock()
        main.has_stock_update = Mock()
        main.has_stock_update.return_value = True
        main.store_stock = Mock()

        main.main()
        main.store_stock.assert_not_called()

    def test_new_stock(self):
        main.logging = Mock()
        main.get_latest_stock_additions = Mock()
        main.display_stock = Mock()
        main.has_stock_update = Mock()
        main.has_stock_update.return_value = False
        main.store_stock = Mock()

        main.main()
        main.store_stock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
