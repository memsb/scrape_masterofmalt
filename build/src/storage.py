import boto3
from datetime import datetime

table_name = 'master_of_malt'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)


def store_stock(stock):
    response = table.put_item(
        Item={
            'date': stock['date'],
            'updated': datetime.now().isoformat(),
            'whiskies': stock['whiskies']
        }
    )
    return response


def has_stock_update(stock):
    response = table.get_item(
        Key={
            'date': stock['date']
        }
    )

    return 'Item' in response
