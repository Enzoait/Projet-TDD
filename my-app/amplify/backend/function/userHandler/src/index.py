import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../common')))

from user_service import get_user

def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    name = body.get('name')

    try:
        user = get_user(name, context)
        # Si l'utilisateur existe, retourne 200
        if user:
            return {
                'statusCode': 200,
                'body': json.dumps(user)
            }
        # Si l'utilisateur n'existe pas, retourne 404
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }
    except Exception as e:
        # Si ValueError ou autre, retourne 400
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }