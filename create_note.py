import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def createNote(event, _context):
    body = json.loads(event['body'])

    note = {
        'noteId': str(uuid.uuid4()),
        'title': body['title'],
        'content': body['content']
    }

    table.put_item(Item=note)

    return {
        'statusCode': 201,
        'body': json.dumps(note)
    }
