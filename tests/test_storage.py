import unittest
from lib import storage
from unittest.mock import Mock, patch


class TestStorage(unittest.TestCase):
    stock = {
        "date": "05-01-2021",
        "whiskies": []
    }

    item_not_found_response = {
        'ResponseMetadata': {
            'RequestId': 'UMUO28BF7P3U1VDO688B4B7T2BVV4KQNSO5AEMVJF66Q9ASUAAJG',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {},
            'RetryAttempts': 0
        }
    }

    item_response = {
        'Item': {
            'date': '05-01-2021',
            'updated': '2021-01-05T15:31:15.688275',
            'whiskies': []
        },
        'ResponseMetadata': {
            'RequestId': '1JEHNVOV0AGGRDHN0JDQ2L4B83VV4KQNSO5AEMVJF66Q9ASUAAJG',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {},
            'RetryAttempts': 0
        }
    }

    @patch('boto3.resource')
    def test_already_has_latest_stock(self, mock_dynamo):
        mock_table = Mock()
        mock_table.get_item.return_value = self.item_response
        mock_dynamo.Table.return_value = mock_table

        has_stock = storage.has_stock_update(self.stock, mock_dynamo)
        self.assertTrue(has_stock)

    @patch('boto3.resource')
    def test_does_not_have_latest_stock(self, mock_dynamo):
        mock_table = Mock()
        mock_table.get_item.return_value = self.item_not_found_response
        mock_dynamo.Table.return_value = mock_table

        has_stock = storage.has_stock_update(self.stock, mock_dynamo)
        self.assertFalse(has_stock)

    @patch('boto3.resource')
    def test_storing_latest_stock(self, mock_dynamo):
        mock_table = Mock()
        mock_dynamo.Table.return_value = mock_table

        storage.store_stock(self.stock, mock_dynamo)
        mock_table.put_item.assert_called_with(Item={
            'date': '05-01-2021',
            'updated': storage.current_time.isoformat(),
            'whiskies': []
        })


if __name__ == '__main__':
    unittest.main()
