import json
import boto3

scheduler_client = boto3.client("scheduler")
SCHEDULE_NAME = "ec2-uptime-cron"

def lambda_handler(event, context):
    response = scheduler_client.update_schedule(
        Name=SCHEDULE_NAME,
        State="ENABLED"
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }