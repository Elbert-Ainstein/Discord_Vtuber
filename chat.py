import os
import openai

from dotenv import load_dotenv
load_dotenv()

apikey = os.getenv('OPENAI_API_KEY')


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = apikey

def gpt3_turbo_completion(conversation, engine='gpt-3.5-turbo', temp=1, tokens=500, stop=None, user=None):
    return openai.ChatCompletion.create(
        model=engine,
        messages=conversation,
        temperature=temp,
        max_tokens=tokens,
        stop=stop
        )['choices'][0]['message']['content']
