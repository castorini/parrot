import argparse
import os
import requests
import sys

from random import randint
from google.cloud import texttospeech
from watson_developer_cloud import TextToSpeechV1


def watson_cloud_tts(text, output_path, username, password):
    voice_list = ['en-US_AllisonVoice', 'en-US_LisaVoice', 'en-US_MichaelVoice', 'en-GB_KateVoice']

    text_to_speech = TextToSpeechV1(
        url='https://stream.watsonplatform.net/text-to-speech/api',
        username=username,
        password=password)

    # Text to speech api request
    for voice in voice_list:
        # Generate random voice characteristics
        random_rate = 'default'
        random_volume = 'default'
        random_pitch = 'default'

        for i in range(10):
            ssml = '<prosody rate="{0}" volume="{1}" pitch="{2}"> {3} </prosody>'.format(random_rate, \
                random_volume, random_pitch, text)
            response = text_to_speech.synthesize(
                ssml,
                accept='audio/wav',
                voice=voice)

            file_name = 'watson_{0}{1}{2}{3}.wav'.format(voice, random_rate, random_volume, random_pitch)
            with open(output_path + '/' + file_name, 'wb') as f:
                f.write(response.content)

            random_rate = str(randint(-15, 15)) + '%'
            random_volume = str(randint(75, 100))
            random_pitch = str(randint(-10, 10)) + 'Hz'

        print('audios in voice ' + voice + ' are created')


def google_cloud_tts(text, output_path):
    voice_list = [('en-GB', 'en-GB-Standard-A'), ('en-GB', 'en-GB-Standard-B'),
    ('en-GB', 'en-GB-Standard-C'), ('en-GB', 'en-GB-Standard-D'),
    ('en-US', 'en-US-Wavenet-A'), ('en-US', 'en-US-Wavenet-B'),
    ('en-US', 'en-US-Wavenet-C'), ('en-US', 'en-US-Wavenet-D'),
    ('en-US', 'en-US-Wavenet-E'), ('en-US', 'en-US-Wavenet-F'),
    ('en-US', 'en-US-Standard-B'), ('en-US', 'en-US-Standard-C'),
    ('en-US', 'en-US-Standard-D'), ('en-US', 'en-US-Standard-E')]

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)

    # Text to speech api request
    for language, voice in voice_list:
        # Generate random voice characteristics
        random_rate = 1
        random_volume = 0
        random_pitch = 0

        for i in range(10):
            voice_config = texttospeech.types.VoiceSelectionParams(
                language_code=language,
                name=voice)
            audio_config = texttospeech.types.AudioConfig(
                audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16,
                speaking_rate=random_rate,
                pitch=random_pitch,
                volume_gain_db=random_volume)

            response = client.synthesize_speech(input_text, voice_config, audio_config)

            file_name = 'gc_{0}{1}%{2}db{3}st.wav'.format(voice, random_rate, random_volume, random_pitch)
            with open(output_path + '/' + file_name, 'wb') as f:
                f.write(response.audio_content)

            random_rate = randint(75, 125)/100
            random_volume = randint(-5, 15)/10
            random_pitch = randint(-50, 50)/10

        print('audios in voice {0} are created'.format(voice))


def microsoft_tts(text, output_path, token):
    voice_list = [('en-AU', 'en-AU, Catherine'), ('en-AU', 'en-AU, HayleyRUS'), 
    ('en-CA', 'en-CA, Linda'), ('en-CA', 'en-CA, HeatherRUS'),
    ('en-GB', 'en-GB, Susan, Apollo'), ('en-GB', 'en-GB, HazelRUS'),
    ('en-GB', 'en-GB, George, Apollo'), ('en-IE', 'en-IE, Sean'),
    ('en-IN', 'en-IN, Heera, Apollo'), ('en-IN', 'en-IN, PriyaRUS'),
    ('en-IN', 'en-IN, Ravi, Apollo'), ('en-US', 'en-US, ZiraRUS'),
    ('en-US', 'en-US, JessaRUS'), ('en-US', 'en-US, BenjaminRUS')]

    # Authentication
    # Text to speech api request
    for language, voice in voice_list:
        # Generate random voice characteristics
        random_rate = str(0) + '%'
        random_volume = str(0) + '%'
        random_pitch = str(0) + 'Hz'

        for i in range(10):
            tts_url = 'https://westus.tts.speech.microsoft.com/cognitiveservices/v1'
            tts_header = {'X-Microsoft-OutputFormat':'riff-16khz-16bit-mono-pcm',
            'Authorization':token,
            'Content-Type':'application/ssml+xml'}

            ssml = '<prosody rate="{0}" volume="{1}" pitch="{2}"> {3} </prosody>'.format(random_rate, \
                random_volume, random_pitch, text)
            tts_content = """<speak version='1.0'
            xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{0}'>
            <voice name='Microsoft Server Speech Text to Speech Voice ({1})'> {2}
            </voice> </speak>""".format(language, voice, ssml)

            tts_response = requests.post(tts_url, headers=tts_header, data=tts_content)

            file_name = 'ms_{0}{1}{2}{3}.wav'.format(voice.replace(' ', ''), random_rate, random_volume, random_pitch)
            with open(output_path + '/' + file_name, 'wb') as f:
                f.write(tts_response.content)

            random_rate = str(randint(-20, 20)) + '%'
            random_volume = str(randint(-20, 20)) + '%'
            random_pitch = str(randint(-15, 15)) + 'Hz'

        print('audios in voice ' + voice + ' are created')


def main():
    parser = argparse.ArgumentParser(description="create a directory for each word, \
        and 320 different voices per word in its directory")
    parser.add_argument('ms_subscription_key', help='Microsoft cognitive service subscription key')
    parser.add_argument('watson_username', help='IBM Watson TTS subscription username')
    parser.add_argument('watson_password', help='IBM Watson TTS subscription password')
    parser.add_argument('--words', nargs='*', help='Words to be pronounced', default=['albert einstein'])
    args = parser.parse_args()

    word_list = args.words

    # Authentication for Microsoft Speech Service
    # Get an authorization token
    # TODO: get a new authentication token per nine minutes
    ms_token_url = 'https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    ms_token_header = {'Ocp-Apim-Subscription-Key':args.ms_subscription_key}
    ms_token_response = requests.post(ms_token_url, headers = ms_token_header)

    for word in word_list:
        # Create an individual directory for each keyword if not existed
        path = word.replace(' ', '')
        if not os.path.exists(path):
            os.makedirs(path)
            print(path + ' directory is created!')

        microsoft_tts(word, path, ms_token_response.text)
        google_cloud_tts(word, path)
        watson_cloud_tts(word, path, args.watson_username, args.watson_password)

        print('all audios for ' + word + ' are generated!')


if __name__ == '__main__':
    main()
