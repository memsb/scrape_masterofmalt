import boto3
from datetime import datetime

table_name = 'master_of_malt'
current_time = datetime.now()


def store_stock(stock, dynamodb=boto3.resource('dynamodb')):
    table = dynamodb.Table(table_name)

    response = table.put_item(
        Item={
            'date': stock['date'],
            'updated': current_time.isoformat(),
            'whiskies': stock['whiskies']
        }
    )
    return response


def has_stock_update(stock, dynamodb=boto3.resource('dynamodb')):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'date': stock['date']
        }
    )

    return 'Item' in response
