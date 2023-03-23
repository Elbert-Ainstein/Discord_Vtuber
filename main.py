import time
import os
from dotenv import load_dotenv
import nltk
import vlc

from twitchio.ext import commands
from google.cloud import texttospeech_v1beta1 as texttospeech
from chat import gpt3_turbo_completion, open_file

try:
    os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
except AttributeError:
    pass

load_dotenv()

twitch_token = os.getenv('TOKEN')


class Bot(commands.Bot):

    conversation = list()

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...

        super().__init__(token=twitch_token, prefix='!',
                         initial_channels=['elbertoainstein'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        # Also check if the message is too long
        if message.echo or len(message.content) > 70:
            return

        # download the words corpus
        nltk.download('words')

        # Check if the message contains english words
        if not any(word in message.content for word in nltk.corpus.words.words()):
            return

        print('------------------------------------------------------')
        print(message.content)
        print(message.author.name)
        print(Bot.conversation)

        Bot.conversation.append(f'CHATTER: {message.content}')
        text_block = '\n'.join(Bot.conversation)
        prompt = open_file('prompt_chat.txt') + text_block
        prompt += '\nDOGGIEBRO: '
        print(prompt)
        response = gpt3_turbo_completion(prompt)
        print('Emily:' , response)
        if not Bot.conversation.count('Emily: ' + response):
            Bot.conversation.append(f'Emily: {response}')
            
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

        vlc.MediaPlayer('output.mp3').play()
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
        open('output.txt', 'w').close()

        # Print the contents of our message to console...

        print('------------------------------------------------------')
        os.remove('output.mp3')

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'twitchtuber-d5f31fbeec60.json'
bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
