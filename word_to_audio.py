import argparse
import os
import requests
import sys

def main():
	parser = argparse.ArgumentParser(description="create a directory for each word, and 15 different voices per word in its directory")
	parser.add_argument('subscription_key', help='Speech service subscription key')
	parser.add_argument('--words', nargs= '*', help='Words to be pronounced')
	args = parser.parse_args()

	word_list = args.words
	voice_list = [('en-AU', 'en-AU, Catherine'), ('en-AU', 'en-AU, HayleyRUS'), ('en-CA', 'en-CA, Linda'), ('en-CA', 'en-CA, HeatherRUS'),
	('en-GB', 'en-GB, Susan, Apollo'), ('en-GB', 'en-GB, HazelRUS'), ('en-GB', 'en-GB, George, Apollo'), ('en-IE', 'en-IE, Sean'),
	('en-IN', 'en-IN, Heera, Apollo'), ('en-IN', 'en-IN, PriyaRUS'), ('en-IN', 'en-IN, Ravi, Apollo'),
	('en-US', 'en-US, ZiraRUS'), ('en-US', 'en-US, JessaRUS'), ('en-US', 'en-US, BenjaminRUS'), ('en-US', 'en-US, JessaRUS')]

	#Authentication
	#get an authorization tocken
	#TODO: get a new authentication token per nine minutes
	token_url = 'https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
	token_header = {'Ocp-Apim-Subscription-Key':args.subscription_key}
	token_response = requests.post(token_url, headers = token_header)

	for word in word_list:
		#create an individual directory for each keyword if not existed
		path = word.replace(' ', '')
		if not os.path.exists(path):
			os.makedirs(path)
			print(path + ' directory is created!')

		#text to speech api request
		#TODO: changing characteristics of generated voice output via SSML
		#https://docs.microsoft.com/en-ca/azure/cognitive-services/Speech/api-reference-rest/bingvoiceoutput#ChangeSSML
		for language, voice in voice_list:
			tts_url = 'https://westus.tts.speech.microsoft.com/cognitiveservices/v1'
			tts_header = {'X-Microsoft-OutputFormat':'riff-24khz-16bit-mono-pcm',
			'Authorization':token_response.text, 'Content-Type':'application/ssml+xml'}
			tts_content = """<speak version='1.0' xmlns="http://www.w3.org/2001/10/synthesis" xml:lang='""" + language + """'>
					<voice  name='Microsoft Server Speech Text to Speech Voice (""" + voice + """)'>""" + word + """</voice> </speak>"""
			tts_response = requests.post(tts_url, headers = tts_header, data = tts_content)

			file_name = voice.replace(' ', '')
			with open(path+'/'+file_name, 'wb') as f:
				f.write(tts_response.content)
				print(path + ' ' + file_name + ' is created!')

		print('---------------------------------')


if __name__ == '__main__':
	main()