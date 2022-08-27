import json
import requests
import AI
import os

auth_token = os.environ.get('SLACK_TOKEN')
header = {'Authorization': f'Bearer {auth_token}'}


class Slack:
    GET_CONVERSATION = 'https://www.slack.com/api/conversations.replies'
    POST_RESPONSE = 'https://www.slack.com/api/chat.postMessage'


def merge_all_messages(messages):
    combined_msg = ''
    for message in messages:
        # print(message['text'])
        combined_msg += message['text'].strip().replace('```', '').replace('\n\n', '\n') + '\n\n'

    print(f"Message: {combined_msg}")
    return combined_msg


def get_conversation(payload):
    if payload.get('thread_ts', None) is None:
        return payload['text']
    else:
        params = {
            'channel': payload['channel'],
            'ts': payload['thread_ts']
        }
        converstation = requests.post(Slack.GET_CONVERSATION, params=params, headers=header)
        data = converstation.json()
        return merge_all_messages(data['messages'])


def lambda_handler(event, context):
    print(f'event: {event} type: {type(event)}')

    for record in event['Records']:
        body = json.loads(record['body'])
        payload = body['event']

        if payload.get('client_msg_id', None) is not None and payload['type'] == 'message':
            text = get_conversation(payload)
            response = AI.get_openai_response(text)
            response_text = AI.get_formatted_response(response)
            # response = AI.mock_code_response()

            data = {
                "text": response_text,
                "channel": payload['channel'],
                "thread_ts": payload['ts']
            }

            requests.post(Slack.POST_RESPONSE, json=data, headers=header)

    return {
        'statusCode': 200
    }
