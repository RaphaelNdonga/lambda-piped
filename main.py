import datetime
import boto3
import json

sns_client = boto3.client("sns")
TOPIC_ARN="arn:aws:sns:eu-west-1:266735808339:ec2-uptime-alert"
SUBJECT="[WARNING]: Excessive usage of EC2 Instance" 
ec2_client = boto3.client("ec2")
MAX_UPTIME_MINS=0

def lambda_handler(event, context):
    response = ec2_client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            launch_time = instance["LaunchTime"]
            instance_state = instance['State']['Name']
            print(instance_id)
            print(launch_time)
            print(instance_state)
            uptime = datetime.datetime.now(tz=launch_time.tzinfo) - launch_time
            uptime_minutes = uptime.total_seconds()/60
            if float(uptime_minutes) > MAX_UPTIME_MINS and instance_state=="running":
                message=f'You cannot afford to have instance {instance_id} running any longer. It\'s been up for {uptime_minutes} minutes'
                sns_client.publish(
                    TopicArn=TOPIC_ARN,
                    Message= message,
                    Subject=SUBJECT
                )
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }