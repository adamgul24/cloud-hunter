import boto3
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    flagged = []
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        try:
            acl = s3.get_bucket_acl(Bucket=bucket_name)
            for grant in acl['Grants']:
                if 'AllUsers' in grant['Grantee'].get('URI', ''):
                    flagged.append(bucket_name)
                    s3.put_bucket_acl(
                        Bucket=bucket_name,
                        ACL='private'
                    )
                    s3.put_bucket_tagging(
                        Bucket=bucket_name,
                        Tagging={
                            'TagSet': [{'Key': 'remediated', 'Value': 'true'}]
                        }
                    )
        except Exception as e:
            continue

    if flagged:
        message = f"[CloudHunter] Public S3 Buckets Auto-Remediated: {flagged}"
        notify(message)

def notify(message):
    sns = boto3.client('sns')
    topic_arn = os.environ.get("ALERT_TOPIC_ARN")
    if topic_arn:
        sns.publish(TopicArn=topic_arn, Message=message, Subject="S3 Exposure - Remediated")
