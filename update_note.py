import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def updateNote(event, _context):
    note_id = event['pathParameters']['noteId']
    body = json.loads(event['body'])

    update_expr_parts = []
    expr_attr_names = {}
    expr_attr_values = {}

    if 'title' in body:
        expr_attr_names['#title'] = 'title'
        expr_attr_values[':newTitle'] = body['title']
        update_expr_parts.append('#title = :newTitle')

    if 'content' in body:
        expr_attr_names['#content'] = 'content'
        expr_attr_values[':newContent'] = body['content']
        update_expr_parts.append('#content = :newContent')

    if 'attachmentUrl' in body:
        expr_attr_names['#attachmentUrl'] = 'attachmentUrl'
        expr_attr_values[':newAttachmentUrl'] = body['attachmentUrl']
        update_expr_parts.append('#attachmentUrl = :newAttachmentUrl')

    if not update_expr_parts:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'no fields to update'})
        }

    table.update_item(
        Key={'noteId': note_id},
        UpdateExpression='SET ' + ', '.join(update_expr_parts),
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Note updated'})
    }
