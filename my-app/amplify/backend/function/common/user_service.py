import boto3
import os

REGION = os.environ.get("REGION", "eu-west-1")
TABLE_NAME = os.environ.get("STORAGE_USERTABLE_NAME", "userTable")

# # Instancier une seule fois
# dynamodb = boto3.resource("dynamodb", region_name=REGION)
# table = dynamodb.Table(TABLE_NAME)

def add_user(name, email, context, called_by):
    print(f"Called by {called_by} : Name : {name} Email : {email}")
    if not name or not email:
        raise ValueError("Missing name or email")
    context[0].put_item(Item={'user_id': name, 'name': name, 'email': email})
    return True

def get_user(name, context):
    if not name:
        raise ValueError("Name is required")
    response = context[0].get_item(Key={'user_id': name})
    # If user not found, return None (do not raise)
    return response.get('Item', None)