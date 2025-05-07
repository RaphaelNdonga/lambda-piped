import boto3
import json

def lambda_handler(event, context):
    ec2_client = boto3.client("ec2")
    response = ec2_client.describe_instances()
    instance_states=[]
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_states.append(instance['State']['Name'] == 'running')
    return {
        "statusCode": 200,
        "body": json.dumps(f'instances: {instance_states}')
    }