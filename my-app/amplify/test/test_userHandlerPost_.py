import pytest
from moto import mock_dynamodb
import boto3
import os

# Fix 1 : Région fixée en haut
os.environ["REGION"] = "eu-west-1"

from backend.function.userHandlerPost.src import index as post_index
from backend.function.common import user_service

TABLE_NAME = os.environ.get("STORAGE_USERTABLE_NAME", "userTable")

@mock_dynamodb
def make_test_table():
    dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
    table = dynamodb.create_table(
        TableName="userTable",
        KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "name", "AttributeType": "S"},
            {"AttributeName": "email", "AttributeType": "S"}
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "email-index",
                "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
            },
            {
                "IndexName": "name-index",
                "KeySchema": [{"AttributeName": "name", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
            }
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
    )
    table.meta.client.get_waiter("table_exists").wait(TableName="userTable")
    return [table, dynamodb]

# @pytest.fixture(autouse=True)
# def dynamodb_mock():
#     with mock_dynamodb():
#         dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
#         dynamodb.create_table(
#             TableName=TABLE_NAME,
#             KeySchema=[{"AttributeName": "name", "KeyType": "HASH"}],
#             AttributeDefinitions=[{"AttributeName": "name", "AttributeType": "S"}],
#             BillingMode="PAY_PER_REQUEST",
#         )
#         yield

@mock_dynamodb
def test_add_user():
    
    ctx = make_test_table()
    event = {
        "body": '{"name": "Alice", "email": "alice@example.com"}'
    }
    response = post_index.handler(event, ctx)
    assert response["statusCode"] == 201

@mock_dynamodb
def test_add_user_missing_fields():
    ctx = make_test_table()
    event = {
        "body": '{"name": "Alice"}'
    }
    response = post_index.handler(event, ctx)
    assert response["statusCode"] == 400
