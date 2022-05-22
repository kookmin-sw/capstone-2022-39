import boto3
import pprint
from boto3.dynamodb.conditions import Attr


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('recruitment-db')


def insert_recruitment(data):
    res = table.put_item(Item=data)
    print(res)


def read_document(filter):
    res = table.scan(
        FilterExpression = Attr('workplace').contains(filter)
    )
    pprint.pprint(res)


if __name__ == '__main__':
    # Test Data
    # data = {
    #     "primary_key": "TestPrimaryKey",
    #     "recruiter": "노인일자리센터",
    # }
    # insert_recruitment(data)
    read_document('마산')