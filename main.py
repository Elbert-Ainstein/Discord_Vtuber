import time
import os
import discord
from discord.ext import commands
import json 
import io
import requests
from IPython.display import Audio, display
from elevenlabslib.helpers import *
from elevenlabslib import *
import time

from chat import gpt3_turbo_completion



token = os.getenv('TOKEN')
labKey = os.getenv('SPEECH_KEY')

user = ElevenLabsUser(labKey)
voice = user.get_voices_by_name("Rachel")[0]


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

with open('prompt_chat.txt') as f:
    conversation = [{"role": "user", "content": f.read()}]
vc = None
@bot.event    
async def on_ready():
    global vc
    # Notify us when everything is ready!
    # We are logged in and ready to chat and use commands...
    print(f'Logged in as | {bot.user.name}')
    vc = await bot.get_channel(889411465788948491).connect()
    print(vc)

@bot.event
async def on_message(message):
    global conversation, vc
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        # Also check if the message is too long
    
    if len(message.content) > 70 or message.author.id == bot.user.id:
        return
    
    # Check if the message contains english words
#    if not any(word in message.con tent for word in nltk.corpus.words.words()):
#        return
    conversation+=[{"role": "user", "content": message.author.name+": "+message.content}]
    response = gpt3_turbo_completion(conversation=conversation)
    await message.channel.send(content=response)
    conversation+=[{"role":"assistant", "content":response}]
    
    with open('tmp.mp3', 'wb') as f:
        f.write(voice.generate_audio_bytes(response))
    
    time.sleep(2)
    if response != None:        
        vc.play(discord.FFmpegPCMAudio('tmp.mp3'))
    print(user.get_history_items())


bot.run(token)
