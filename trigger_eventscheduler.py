import json
import boto3

scheduler_client = boto3.client("scheduler")
SCHEDULE_NAME = "ec2-uptime-cron"

def lambda_handler(event, context):
    current = scheduler_client.get_schedule(
        Name=SCHEDULE_NAME
    )
    response = scheduler_client.update_schedule(
        Name=SCHEDULE_NAME,
        FlexibleTimeWindow=current["FlexibleTimeWindow"],
        ScheduleExpression=current["ScheduleExpression"],
        Target=current["Target"],
        State="ENABLED"
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }