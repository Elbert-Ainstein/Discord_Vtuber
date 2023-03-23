import openai
import os
from dotenv import load_dotenv
load_dotenv()

apikey = os.getenv('KEY')

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = apikey


def gpt3_completion(prompt, engine='text-davinci-003', temp=0.9, tokens=400, freq_pen=2.0, pres_pen=2.0, stop=['DOGGIEBRO:', 'CHATTER:']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text






