import time
import os
#import nltk
from gtts import gTTS
import discord
from discord.ext import commands


#from google.cloud import texttospeech_v1beta1 as texttospeech
from chat import gpt3_turbo_completion



token = os.getenv('TOKEN')

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
    vc = await bot.get_channel(889411465788948490).connect()
    print(vc)
#nltk.download('words')

@bot.event
async def on_message(message):
    global conversation, vc
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        # Also check if the message is too long
    
    if len(message.content) > 70 or message.author.id == bot.user.id:
        return
    
    # Check if the message contains english words
#    if not any(word in message.content for word in nltk.corpus.words.words()):
#        return
    conversation+=[{"role": "user", "content": message.author.name+": "+message.content}]
    response = gpt3_turbo_completion(conversation=conversation)
    await message.reply(content=response)
    conversation+=[{"role":"assistant", "content":response}]
    tts = gTTS(response, lang='en', tld='us')
    tts.save('tmp.mp3')
    vc.play(discord.FFmpegPCMAudio('tmp.mp3',executable=os.getenv('FFMPEG_LOC')))

    """
        client = texttospeech.TextToSpeechClient()

        response = message.content + "? " + response
        ssml_text = '<speak>'
        response_counter = 0
        mark_array = []
        for s in response.split(' '):
            ssml_text += f'<mark name="{response_counter}"/>{s}'
            mark_array.append(s)
            response_counter += 1
        ssml_text += '</speak>'

        input_text = texttospeech.SynthesisInput(ssml=ssml_text)

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-GB",
            name="en-GB-Wavenet-B",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice,
                     "audio_config": audio_config, "enable_time_pointing": ["SSML_MARK"]}
        )

        # The response's audio_content is binary.
        with open("output.mp3", "wb") as out:
            out.write(response.audio_content)

        # playsound(audio_file, winsound.SND_ASYNC)

        count = 0
        for i in range(len(response.timepoints)):
            count += 1
            with open("output.txt", "a", encoding='utf-8') as out:
                out.write(
                    mark_array[int(response.timepoints[i].mark_name)] + " ")
            if i != len(response.timepoints) - 1:
                total_time = response.timepoints[i + 1].time_seconds
                time.sleep(total_time - response.timepoints[i].time_seconds)
            if count == 25:
                open('output.txt', 'w', encoding='utf-8').close()
                count = 0
            elif count % 7 == 0:
                with open("output.txt", "a", encoding='utf-8') as out:
                    out.write("\n")
        
        time.sleep(2)
        open('output.txt', 'w', encoding='utf-8').close()

        # Print the contents of our message to console...

        print('------------------------------------------------------')
        os.remove('output.mp3')
        """



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'twitchtuber-d5f31fbeec60.json'
bot.run(token)
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
