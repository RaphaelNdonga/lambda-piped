import boto3
import json

def lambda_handler(event, context):
    ec2_client = boto3.client("ec2")
    response = ec2_client.describe_instances()
    return {
        "statusCode": 200,
        "body": json.dumps(f'instances: {response}')
    }