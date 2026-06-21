import json
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = 'notes-attachments-thienban'

def getUploadUrl(event, _context):
    note_id = event['pathParameters']['noteId']
    filename = event['queryStringParameters']['filename']

    key = f"{note_id}/{filename}"

    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key},
        ExpiresIn=300
    )

    file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"

    return {
        'statusCode': 200,
        'body': json.dumps({
            'uploadUrl': presigned_url,
            'fileUrl': file_url
        })
    }
