import datetime
import boto3
import json

SCHEDULE_NAME = "ec2-uptime-cron"
scheduler_client = boto3.client("scheduler")
sns_client = boto3.client("sns")
TOPIC_ARN="arn:aws:sns:eu-west-1:266735808339:ec2-uptime-alert"
SUBJECT="[WARNING]: Excessive usage of EC2 Instance" 
ec2_client = boto3.client("ec2")
MAX_UPTIME_MINS=15

def lambda_handler(event, context):
    response = ec2_client.describe_instances()
    running_instances=[]
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            launch_time = instance["LaunchTime"]
            instance_state = instance['State']['Name']
            print(instance_id)
            print(launch_time)
            print(instance_state)
            if instance_state != "running":
                continue

            # all instances beyond this point are running
            running_instances.append(instance_id)
            uptime = datetime.datetime.now(tz=launch_time.tzinfo) - launch_time
            uptime_minutes = uptime.total_seconds()/60
            if float(uptime_minutes) > MAX_UPTIME_MINS:
                message=f'You cannot afford to have instance {instance_id} running any longer. It\'s been up for {uptime_minutes} minutes'
                sns_client.publish(
                    TopicArn=TOPIC_ARN,
                    Message= message,
                    Subject=SUBJECT
                )
    # if 0 running instances, disable the cronjob of the eventbridge scheduler
    if len(running_instances) < 1:
            current = scheduler_client.get_schedule(
                 Name=SCHEDULE_NAME
            )

            scheduler_client.update_schedule(
                Name=SCHEDULE_NAME,
                FlexibleTimeWindow=current["FlexibleTimeWindow"],
                ScheduleExpression=current["ScheduleExpression"],
                Target=current["Target"],
                State="DISABLED"
            )

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }