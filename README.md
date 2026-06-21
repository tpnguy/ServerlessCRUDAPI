# Serverless CRUD API

A fully serverless REST API for managing notes, built on AWS. No servers to maintain — Lambda functions handle compute, DynamoDB handles storage, and API Gateway exposes everything over HTTP.

## AWS Services Used

| Service | Role |
| --- | --- |
| **API Gateway** | Routes HTTP requests to the right Lambda function |
| **AWS Lambda** | Runs the business logic for each CRUD operation |
| **DynamoDB** | Stores notes as key-value items |
| **S3** | Stores file attachments; presigned URLs let clients upload directly |
| **IAM** | Controls what each Lambda is allowed to do |
| **CloudWatch** | Captures Lambda logs for debugging |

## Endpoints

Base URL: `https://35evhy42hc.execute-api.us-east-1.amazonaws.com/prod`

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/notes` | Create a new note |
| `GET` | `/notes/{noteId}` | Get a note by ID |
| `PUT` | `/notes/{noteId}` | Update a note's title, content, or attachment |
| `DELETE` | `/notes/{noteId}` | Delete a note |
| `GET` | `/notes/{noteId}/upload?filename=` | Get a presigned S3 URL to upload a file attachment |

## Request & Response Examples

### Create a note

```json
POST /notes
Content-Type: application/json

{
  "title": "My Note",
  "content": "Hello world"
}
```

Returns the created note with a generated `noteId`.

### Update a note

```json
PUT /notes/{noteId}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content",
  "attachmentUrl": "https://..."
}
```

All fields are optional — only include what you want to change.

### Upload a file attachment

```text
1. GET /notes/{noteId}/upload?filename=mydoc.pdf
   → returns { uploadUrl, fileUrl }

2. PUT {uploadUrl}
   Body: raw file bytes (no Content-Type header)

3. PUT /notes/{noteId}
   Body: { "attachmentUrl": "{fileUrl}" }
```

## Project Structure

```text
├── create_note.py       # POST /notes
├── read_note.py         # GET /notes/{noteId}
├── update_note.py       # PUT /notes/{noteId}
├── delete_note.py       # DELETE /notes/{noteId}
├── get_upload_url.py    # GET /notes/{noteId}/upload
└── chapt1.py            # One-time DynamoDB table setup
```

## IAM Setup

The Lambda functions share a single execution role with:

- `AmazonDynamoDBFullAccess`
- `AmazonS3FullAccess`
- `AWSLambdaBasicExecutionRole`
