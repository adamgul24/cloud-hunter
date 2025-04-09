import boto3
import datetime
import os

def log_to_dynamo(event_type, details):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv("DYNAMO_TABLE", "CloudHunterThreatLogs"))
    table.put_item(Item={
        "event_id": f"{event_type}-{datetime.datetime.utcnow().isoformat()}",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "type": event_type,
        "details": details
    })
