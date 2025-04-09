import boto3
import os

def send_alert(message, subject="CloudHunter Alert"):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=os.getenv("ALERT_TOPIC_ARN"),
        Message=message,
        Subject=subject
    )
