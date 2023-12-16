import boto3
from botocore.exceptions import ClientError

# DynamoDB에 연결하기 위한 함수
def dynamodb_connection():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb

# 테이블에서 모든 데이터를 스캔하는 함수
def scan_table():
    try:
        dynamodb = dynamodb_connection()
        table = dynamodb.Table('test')
        response = table.scan()
        return response['Items']
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

# 특정 항목을 조회하는 함수 (예: 특정 ID에 해당하는 데이터 조회)
def get_item(item_key):
    try:
        dynamodb = dynamodb_connection()
        table = dynamodb.Table('test')
        response = table.get_item(Key=item_key)
        return response.get('Item', None)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
