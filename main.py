import datetime
import boto3
import json

def lambda_handler(event, context):
    sns_client = boto3.client("sns")
    ec2_client = boto3.client("ec2")
    response = ec2_client.describe_instances()
    instance_states=[]
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

            message=f'You cannot afford to have instance {instance_id} running any longer. It\'s been up for {uptime_minutes} minutes'
            subject="[WARNING]: Excessive usage of EC2 Instance" 
            sns_client.publish(
                TopicArn="arn:aws:sns:eu-west-1:266735808339:ec2-uptime-alert",
                Message= message,
                Subject=subject
            )
    return {
        "statusCode": 200,
        "body": json.dumps(f'instances: {instance_states}')
    }