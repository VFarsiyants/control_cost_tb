import json
import os

import openai

def ai_request(query: str, func: dict, return_argument: str):
    '''Sends request to gpt and return answer of gpt
    '''
    if os.getenv('OPEN_AI_KEY') is None:
        return

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=[{'role': 'user', 'content': query}],
        functions=[func],
    function_call={'name': func['name']},
    )

    reply_content = completion.choices[0].message

    funcs = reply_content.to_dict()['function_call']['arguments']
    funcs = json.loads(funcs)

    return funcs[return_argument]
