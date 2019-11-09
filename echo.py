
import json
# This is primarily used for using the supported language list
import random
# This is used for picking a random language when it's not specified
import stat
# This is used to make ffmpeg executable
import requests
# This is used to grab/save the mp3 file from google
import os
# This is for granting ffmpeg executable permissions
import tinys3
from keys import *
import random
import boto3
from contextlib import closing
from twilio.rest import Client
import os

account_sid = TWILIO_ID
auth_token = TWILIO_AUTH

def gen_guid():
	return ''.join([str(random.randint(1,9)) for i in range(10)])

def create_mp3(text, uuid):
	client = boto3.client('polly',aws_access_key_id=AMAZON_ACCESS_KEY,
	aws_secret_access_key=AMAZON_SECRET_KEY,region_name='us-east-2')

	response = client.synthesize_speech(
		OutputFormat='mp3',
		Text=text,
		TextType='text',
		VoiceId='Salli'
	)

	if "AudioStream" in response:
		with closing(response["AudioStream"]) as stream:
			output = "{}.mp3".format(uuid)

			try:
				# Open a file for writing the output as a binary stream
				with open(output, "wb") as file:
					file.write(stream.read())
			except IOError as error:
				# Could not write to file, exit gracefully
				print(error)
				sys.exit(-1)
		uploadFile(output)
	return "https://echolinguistics.s3.amazonaws.com/{}.mp3".format(uuid)

def returnSSMLResponse(ssmlFile, endSession=True):
	# This is the full *completed* response that's sent to the client
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			"outputSpeech":
			{
				  "type": "SSML",
				  "ssml": "<speak><audio src='{}'/></speak>".format(SSML_URL.format(ssmlFile))
					},
					"shouldEndSession": endSession
				  }
		}

def make_call(phoneNumber, uuid):
	client = Client(account_sid, auth_token)
	urlVal = "https://echolinguistics.s3.amazonaws.com/{}.xml".format(uuid)
	print(urlVal)
	call = client.calls.create(
							method= 'GET',
	                        url=urlVal,
	                        to='+1{}'.format(phoneNumber),
	                        from_='+14153160468'
	                    )

	print(call.sid)

def create_twiml(uuid):
	echo = """<Response>
	<Play>https://echolinguistics.s3.amazonaws.com/{}.mp3</Play>
	</Response>""".format(uuid)
	file1 = open("{}.xml".format(uuid),"w")
	file1.write(echo) 
	file1.close()
	uploadFile("{}.xml".format(uuid))
		

def uploadFile(fileName):
	bucketID = tempBucketID
	# This converts the bucketID from "https://s3.amazonaws.com/bucketid/" to "bucketid"
	finalFileName = fileName.split('/')[-1]
	# Converts the input from /whateverinput/ to whateverinput
	conn = tinys3.Connection(AMAZON_ACCESS_KEY,AMAZON_SECRET_KEY,tls=True)
	# This open up the s3 conneciton using the constants defined at the beginning
	# TODO - Ideally this would be a class that would take these vars on input and test...
	conn.upload(finalFileName, open(fileName,'rb'), bucketID)


def create_upload_text(restaraunt):
	uuid = gen_guid()
	text = """You are trying to book a table at {}
	thank you, but it seems like nothing is currently available""".format(restaraunt)
	create_mp3(text, uuid)
	create_twiml(uuid)
	make_call("8645674106", uuid)
	os.system('rm {}*'.format(uuid))


if __name__ == '__main__':
	create_upload_text("veggie grille")

######### This runs anytime echoLinguistics.py is imported  #######################
# createmp3List()
# This creates the list of mp3 files that have already been generated

#uploadFile("temp.txt")