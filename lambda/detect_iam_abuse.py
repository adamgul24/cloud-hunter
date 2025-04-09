import boto3
import os
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    client = boto3.client('cloudtrail')
    now = datetime.utcnow()
    past = now - timedelta(minutes=30)

    response = client.lookup_events(
        LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'ConsoleLogin'}],
        StartTime=past,
        EndTime=now,
        MaxResults=50
    )

    flagged = []
    for event in response['Events']:
        data = json.loads(event['CloudTrailEvent'])
        if data.get('responseElements') is None:
            flagged.append({
                'username': data['userIdentity'].get('userName'),
                'time': event['EventTime'],
                'sourceIP': data.get('sourceIPAddress')
            })

    if flagged:
        message = f"[CloudHunter] Failed ConsoleLogin attempts detected: {json.dumps(flagged, indent=2)}"
        notify(message)

def notify(message):
    sns = boto3.client('sns')
    topic_arn = os.environ.get("ALERT_TOPIC_ARN")
    if topic_arn:
        sns.publish(TopicArn=topic_arn, Message=message, Subject="IAM Abuse Detected")
