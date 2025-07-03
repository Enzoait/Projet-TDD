import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../common')))

from user_service import add_user

def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    name = body.get('name')
    email = body.get('email')
    try:
        add_user(name, email, context, "handlerPost")
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'User created'})
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }