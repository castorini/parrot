import argparse
import os
import requests
import sys

from random import randint

def main():
    parser = argparse.ArgumentParser(description="create a directory for each word, \
        and 84 different voices per word in its directory")
    parser.add_argument('subscription_key', help='Speech service subscription key')
    parser.add_argument('--words', nargs= '*', help='Words to be pronounced', default=['albert einstein'])
    args = parser.parse_args()

    word_list = args.words
    voice_list = [('en-AU', 'en-AU, Catherine'), ('en-AU', 'en-AU, HayleyRUS'), 
    ('en-CA', 'en-CA, Linda'), ('en-CA', 'en-CA, HeatherRUS'),
    ('en-GB', 'en-GB, Susan, Apollo'), ('en-GB', 'en-GB, HazelRUS'),
    ('en-GB', 'en-GB, George, Apollo'), ('en-IE', 'en-IE, Sean'),
    ('en-IN', 'en-IN, Heera, Apollo'), ('en-IN', 'en-IN, PriyaRUS'),
    ('en-IN', 'en-IN, Ravi, Apollo'), ('en-US', 'en-US, ZiraRUS'),
    ('en-US', 'en-US, JessaRUS'), ('en-US', 'en-US, BenjaminRUS')]

    # Authentication
    # Get an authorization token
    # TODO: get a new authentication token per nine minutes
    token_url = 'https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    token_header = {'Ocp-Apim-Subscription-Key':args.subscription_key}
    token_response = requests.post(token_url, headers = token_header)

    for word in word_list:
        # Create an individual directory for each keyword if not existed
        path = word.replace(' ', '')
        if not os.path.exists(path):
            os.makedirs(path)
            print(path + ' directory is created!')

        # Text to speech api request
        for language, voice in voice_list:
            # Generate random voice characteristics
            random_rate = str(0) + '%'
            random_volume = str(0) + '%'
            random_pitch = str(0) + 'Hz'

            for i in range(6):
                tts_url = 'https://westus.tts.speech.microsoft.com/cognitiveservices/v1'
                tts_header = {'X-Microsoft-OutputFormat':'riff-16khz-16bit-mono-pcm',
                'Authorization':token_response.text,
                'Content-Type':'application/ssml+xml'}
                tts_content = """<speak version='1.0'
                xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{0}'>
                <voice name='Microsoft Server Speech Text to Speech Voice ({1})'>
                <prosody rate="{2}" volume="{3}" pitch="{4}"> {5} </prosody>
                </voice> </speak>""".format(language, voice, random_rate, \
                    random_volume, random_pitch, word)
                tts_response = requests.post(tts_url, headers = tts_header, data = tts_content)

                file_name = voice.replace(' ', '') + random_rate + random_volume + random_pitch 
                with open(path + '/' + file_name, 'wb') as f:
                    f.write(tts_response.content)
                    print(path + ' ' + file_name + ' is created!')

                random_rate = str(randint(-20, 20)) + '%'
                random_volume = str(randint(-20, 20)) + '%'
                random_pitch = str(randint(-20, 20)) + 'Hz'

        print('---------------------------------')


if __name__ == '__main__':
    main()
