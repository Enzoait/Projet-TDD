import pytest
from moto import mock_dynamodb
import boto3
import os

# Fix 1 : Région fixée en haut
os.environ["REGION"] = "eu-west-1"

from backend.function.userHandler.src import index as get_index
from backend.function.common import user_service

TABLE_NAME = os.environ.get("STORAGE_USERTABLE_NAME", "userTable")

@mock_dynamodb
def make_test_table() -> list:
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

    # Force user_service to use the mocked table
    # user_service.dynamodb = dynamodb
    # user_service.table = table

    return [table, dynamodb]


# @mock_dynamodb
# def test_add_and_get_user_by_email():
#     make_test_table()

@mock_dynamodb
def test_get_user():
    ctx = make_test_table()
    name = "Bob"
    email = "bob@example.com"
    user_service.add_user(name, email, ctx, "test_get_user")
    event = {
       "body" : '{"name": "Bob"}'
    }
    response = get_index.handler(event, ctx)
    if response["statusCode"] != 200:
        print(f"Test get_user failed with response: {response}")
    assert response["statusCode"] == 200
    assert "bob@example.com" in response["body"]

@mock_dynamodb
def test_get_user_not_found():
    
    ctx = make_test_table()
    event = {
        "body" : '{"name": "Charlie"}'
    }
    response = get_index.handler(event, ctx)
    if response["statusCode"] != 404:
        print(f"Test get_user failed with response: {response}")
    assert response["statusCode"] == 404

@mock_dynamodb
def test_get_user_missing_param():
    ctx = make_test_table()
    event = {
        "body" : '{}'
    }
    response = get_index.handler(event, ctx)
    assert response["statusCode"] == 400
