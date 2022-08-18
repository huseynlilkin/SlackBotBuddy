import json
import requests
import AI
import os


def lambda_handler(event, context):
    print(f'event: {event} type: {type(event)}')

    url = 'https://www.slack.com/api/chat.postMessage'
    auth_token = os.environ.get('SLACK_TOKEN')
    header = {'Authorization': f'Bearer {auth_token}'}

    for record in event['Records']:
        print(f'Record: {record}')
        payload = json.loads(record['body'])['event']
        print(f'Payload: {payload}')

        if payload.get('client_msg_id', None) is not None and payload['type'] == 'message':
            print(f"request message to openai is: {payload['text']}")
            response = AI.get_formatted_response(payload['text'])

            print("Creating response")
            data = {
                "text": response,
                "channel": payload['channel'],
                "thread_ts": payload['ts']
            }

            requests.post(url, json=data, headers=header)

    return {
        'statusCode': 200
    }
