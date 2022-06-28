try:
 import unzip_requirements
except ImportError:
 pass
import boto3
import os
import json

s3 = boto3.client('s3')

def handler(event, context):
    print(os.environ['BUCKET_NAME'])
    print(event["pathParameters"]["key"]) 
    url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': os.environ['BUCKET_NAME'],
                'Key': event["pathParameters"]["key"],
                 'ContentType': 'image/png'
            },
            ExpiresIn=24 * 3600
        )
    body = {
        "url": url,
    }

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
             "Access-Control-Allow-Origin": "*"
         },
        "body": json.dumps(body)
    }

    return response