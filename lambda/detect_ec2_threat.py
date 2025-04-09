import boto3
import os
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    flagged_instances = []

    now = datetime.now(timezone.utc)
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == 'running':
                launch_time = instance['LaunchTime']
                age_minutes = (now - launch_time).total_seconds() / 60
                if age_minutes < 30 and instance.get('Tags') is None:
                    flagged_instances.append(instance['InstanceId'])
                    ec2.create_tags(Resources=[instance['InstanceId']], Tags=[{'Key': 'flagged', 'Value': 'rogue'}])
                    try:
                        ec2.stop_instances(InstanceIds=[instance['InstanceId']])
                    except Exception as e:
                        pass

    if flagged_instances:
        message = f"[CloudHunter] EC2 Auto-Isolated (Stopped + Tagged): {flagged_instances}"
        notify(message)

def notify(message):
    sns = boto3.client('sns')
    topic_arn = os.environ.get("ALERT_TOPIC_ARN")
    if topic_arn:
        sns.publish(TopicArn=topic_arn, Message=message, Subject="EC2 Rogue - Remediated")
