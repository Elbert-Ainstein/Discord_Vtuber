import os
import openai

from dotenv import load_dotenv
load_dotenv()

apikey = os.getenv('OPENAI_API_KEY')


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = apikey

stopSequences = ['Emily:',
                 'CHATTER:', 
                 f'CHATTER{list(range(2, 1001))}: ', 
                ]

def gpt3_turbo_completion(prompt, engine='gpt-3.5-turbo', temp=1, tokens=500, stop=None):
    stop = stop or stopSequences
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.ChatCompletion.create(
        model=engine,
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        temperature=temp,
        max_tokens=tokens,
        stop=stop,
        )
    text = response['choices'][0]['message']['content']
    return text
