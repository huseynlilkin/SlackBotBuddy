import json
import requests
import AI
import os

auth_token = os.environ.get('SLACK_TOKEN')
header = {'Authorization': f'Bearer {auth_token}'}


class Slack:
    GET_CONVERSATION = 'https://www.slack.com/api/conversations.replies'
    POST_RESPONSE = 'https://www.slack.com/api/chat.postMessage'


def get_conversation(payload):
    params = {
        'channel': payload['channel'],
        'thread_ts': payload['ts']
    }
    converstation = requests.post(Slack.GET_CONVERSATION, params=params, headers=header)
    print(f"Converstation: {converstation}")


def lambda_handler(event, context):
    print(f'event: {event} type: {type(event)}')

    for record in event['Records']:
        print(f'Record: {record}')
        payload = json.loads(record['body'])['event']
        print(f'Payload: {payload}')

        if payload.get('client_msg_id', None) is not None and payload['type'] == 'message':
            print(f"request message to openai is: {payload['text']}")
            # response = AI.get_formatted_response(payload['text'])

            get_conversation(payload)
            response = AI.mock_code_response()

            print("Creating response")
            data = {
                "text": response,
                "channel": payload['channel'],
                "thread_ts": payload['ts']
            }

            requests.post(Slack.POST_RESPONSE, json=data, headers=header)

    return {
        'statusCode': 200
    }
