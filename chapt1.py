import boto3
import json
import uuid

TABLE_NAME = 'Notes'

session = boto3.Session(profile_name='Thienban')
dynamodb = session.client('dynamodb')
dynamodb_resource = session.resource('dynamodb')
table = dynamodb_resource.Table(TABLE_NAME)

# Create the table if it doesn't already exist
try:
    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'noteId',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'noteId',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    print("Table created, waiting for it to become active...")
    dynamodb.get_waiter('table_exists').wait(TableName=TABLE_NAME)
    print("Table is ready.")
except dynamodb.exceptions.ResourceInUseException:
    print("Table already exists, skipping creation.")

response = dynamodb.describe_table(TableName=TABLE_NAME)
print(f"Item count: {response['Table']['ItemCount']}")






def updateNote(event, _context):
    body = json.loads(event["body"])
    note_id = body['noteId']

    update_expr_parts = []
    expr_attr_names = {}
    expr_attr_values = {}

    if "title" in body:
        expr_attr_names["#title"] = "title"
        expr_attr_values[":newTitle"] = body["title"]
        update_expr_parts.append("#title = :newTitle")

    if "content" in body:
        expr_attr_names["#content"] = "content"
        expr_attr_values[":newContent"] = body["content"]
        update_expr_parts.append("#content = :newContent")
    
    if not update_expr_parts:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "no fields to update"
            })
        }

    update_expression = "SET " + ", ".join(update_expr_parts)

    table.update_item(
        Key={
            'noteId': note_id
        },
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
        UpdateExpression=update_expression
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Note updated'})
    }
    
def deleteNote(event, _context):
    body = json.loads(event['body'])
    note_id = body['noteId']
    
    response = table.get_item(
        Key={'noteId': note_id}
    )

    note = response.get('Item')
    if not note:
        return {'statusCode': 404, 'body': json.dumps({'error': 'Note not found'})}

    table.delete_item(
        Key={
            "noteId": note_id
        }
    )
    return {"statusCode": 204, "body": json.dumps({
        "message": "Note deleted"
    })}

# Expose all four lambda expressions via API Gateway (REST endpoints)

# Secure with IAM execution roles (Lambda -> DynamoDB only)

# Test with Curl or Postman, watch logs in CloudWatch

# Stretch: Add S3 file attachments (store file, return URL in note)

if __name__ == '__main__':
    fake_event = {
        'body': json.dumps({
            'noteId': '92815e8d-6818-4ff2-ab12-511c7d5bba24'
        })
    }
    print(deleteNote(fake_event, None))
