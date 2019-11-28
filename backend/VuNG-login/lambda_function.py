import json
import uuid
import os
import boto3
from datetime import datetime, timedelta

DYNAMODB_USER = os.environ['DYNAMODB_USER']
EXPIRE_IN_SECOND = os.environ['EXPIRE_IN_SECOND']

client_dynamo = boto3.client('dynamodb')

ERRORS = {}
ERRORS['BAD_FORMAT'] = {
    'result': 'error',
    'body': 'Invalid format of request'
}

ERRORS['SIGNUP_ERROR_0'] = {
    'result': 'error',
    'body': 'username existed or password invalid'
}

ERRORS['LOGIN_ERROR_0'] = {
    'result': 'error',
    'body': 'Invalid username or password'
}
ERRORS['LOGIN_ERROR_1'] = {
    'result': 'error',
    'body': 'Account not yet approved'
}

def getUserByUsername(username):
    data = client_dynamo.scan(
        TableName=DYNAMODB_USER,
        ScanFilter={
            'username':{
                'AttributeValueList':[
                    {
                        'S': username
                    }
                ],
                'ComparisonOperator': 'EQ'
            }
        },
        ConsistentRead=True
    )
    print ('>> getUser : ')
    print (json.dumps(data))
    
    if len(data['Items']) != 1:
        return None
    else:
        return data['Items'][0]

def signup(username, password):
    user=getUserByUsername(username)
    if user is not None:
        return ERRORS['SIGNUP_ERROR_0']
    if len(password) < 8:
        return ERRORS['SIGNUP_ERROR_0']
    
    userId = str(uuid.uuid1())
    client_dynamoresponse = client_dynamo.put_item(
        TableName=DYNAMODB_USER,
        Item={
            'userId': {
                'S': userId
            },
            'username': {
                'S': username
            },
            'password': {
                'S': password
            },
            'role': {
                'N': '0'
            },
            'status': {
                'BOOL': False
            }
        },
        ReturnValues='NONE',
        ReturnConsumedCapacity='TOTAL'
    )
    
    return {
        'result': 'ok'
    }

def login(username, password):
    user=getUserByUsername(username)
    if user is None:
        return ERRORS['LOGIN_ERROR_0']
    
    dbPassword = user['password']['S']
    if password != dbPassword:
        return ERRORS['LOGIN_ERROR_0']
    
    dbStatus = user['status']['BOOL']
    if dbStatus == False:
        return ERRORS['LOGIN_ERROR_1']
    
    expireTime = datetime.now(tz=None) + timedelta(seconds=int(EXPIRE_IN_SECOND))
    token = {
        "userId":user['userId']['S'],
        "role":int(user['role']['N']),
        "exp":str(expireTime)
    }
    
    return {
        'result': 'ok',
        'body': json.dumps({
            'token': json.dumps(token)
        })
    }
    

def lambda_handler(event, context):
    if event is None:
        return ERRORS['BAD_FORMAT']
    print ('>> Event : ')
    print (json.dumps(event))
    
    requestType = ''
    username = ''
    password = ''
    try:
        requestType = event['type']
        username = event['username']
        password = event['password']
        if (username is None or password is None or requestType is None):
            return ERRORS['LOGIN_ERROR_0']
    except Exception as e:
        return ERRORS['BAD_FORMAT']
    
    if requestType == 'Signup':
        return signup(username, password)
    
    if requestType == 'Login':
        return login(username, password)

