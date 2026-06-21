import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def deleteNote(event, _context):
    note_id = event['pathParameters']['noteId']

    response = table.get_item(
        Key={'noteId': note_id}
    )

    if not response.get('Item'):
        return {'statusCode': 404, 'body': json.dumps({'error': 'Note not found'})}

    table.delete_item(
        Key={'noteId': note_id}
    )

    return {
        'statusCode': 204,
        'body': json.dumps({'message': 'Note deleted'})
    }
