import openai
import json
import os

openai.api_key = os.environ.get('OPENAI_TOKEN')


def get_openai_response(message):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=message,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response


def get_formatted_response(message):
    response = get_openai_response(message)
    print(f"OpenAI response: {json.dumps(response)}")

    return f"```{response['choices'][0]['text'].strip()}```"
