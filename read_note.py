import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def readNote(event, _context):
    note_id = event['pathParameters']['noteId']

    response = table.get_item(
        Key={'noteId': note_id}
    )

    note = response.get('Item')
    if not note:
        return {'statusCode': 404, 'body': json.dumps({'error': 'Note not found'})}

    return {
        'statusCode': 200,
        'body': json.dumps(note)
    }
