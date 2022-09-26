import json
import os

import boto3


def is_verified_source(payload):
    # This is deprecated but easy way of verification
    return payload.get('token', '') == os.environ.get('VERIFICATION_TOKEN')


def is_valid_request(payload):
    return payload.get('client_msg_id', None) is not None and payload['type'] == 'message'


def lambda_handler(event, context):
    body = json.loads(event['body'])

    if is_verified_source(body) and is_valid_request(body['event']):
        sqs = boto3.client('sqs')
        sqs.send_message(
            QueueUrl=os.environ.get('SQS_URL'),
            MessageBody=json.dumps(body)
        )

    return {
        'statusCode': 200
    }
