import json
import boto3
import base64
import os
import uuid
from datetime import datetime

S3_BUCKET_UPLOAD_IMAGE = os.environ['S3_BUCKET_UPLOAD_IMAGE']

client_s3 = boto3.client('s3')

def putObjectToS3(data):
    print ('>> putObjectToS3')
    
    # Generate file name 
    originalNameAndExt = data['name']
    dividerIdx = originalNameAndExt.rfind('.')
    originalName = originalNameAndExt[:dividerIdx]
    ext = originalNameAndExt[dividerIdx:]
    time = str(datetime.now().timestamp())
    fileName = originalName + '_' + time + ext

    # Generate file data
    originalData = data['file']
    dividerIdx = originalData.rfind(',')
    fileType = originalData[:dividerIdx]
    dividerIdxPlus1 = dividerIdx + 1
    fileData = base64.b64decode(originalData[dividerIdxPlus1:])

    response = client_s3.put_object(
        Bucket=S3_BUCKET_UPLOAD_IMAGE,
        Key=fileName,
        Body=fileData
    )
    print (response)

def lambda_handler(event, context):
    print ('>> EVENT')
    # print (json.dumps(event))
    
    putObjectToS3(event)
    return {
        'result': 'ok'
    }
