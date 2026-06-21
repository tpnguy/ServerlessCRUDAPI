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

# Expose all four lambda expressions via API Gateway (REST endpoints)

# Secure with IAM execution roles (Lambda -> DynamoDB only)

# Test with Curl or Postman, watch logs in CloudWatch

# Stretch: Add S3 file attachments (store file, return URL in note)
    
    
