
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

headers = {
'authorization': "Bearer {}".format(API_KEY),
'cache-control': "no-cache",
}

PHONE_CALL_SCRIPT = """
I am calling on behalf of {0} who has requested a reservation at {1} on {2} at {3}.
Press the pound sign to confirm this reservation, or 2 to be forwarded to the customer.
"""

def log(string):
	print(string)

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
			output = "/tmp/{}.mp3".format(uuid)

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

def create_twiml(uuid, personalPhone):
	echo = """<Response>
	<Play>https://echolinguistics.s3.amazonaws.com/welcome.mp3</Play>
	<Gather timeout="10" numDigits="1" method="GET" action="https://echolinguistics.s3.amazonaws.com/{0}_2.xml">
    </Gather>
	<Play>https://echolinguistics.s3.amazonaws.com/{0}.mp3</Play>
	<Gather timeout="10" numDigits="1" method="GET" action="https://echolinguistics.s3.amazonaws.com/{0}_2.xml">
    </Gather>
    <Play>https://echolinguistics.s3.amazonaws.com/ending.mp3</Play>
    <Pause length="1"/>
	</Response>""".format(uuid)
	echo2 = """
		<Response>
		    <Dial>{}</Dial>
		</Response>
	""".format(personalPhone)
	file1 = open("/tmp/{}.xml".format(uuid),"w")
	file1.write(echo) 
	file1.close()
	uploadFile("/tmp/{}.xml".format(uuid))
	file2 = open("/tmp/{}_2.xml".format(uuid),"w")
	file2.write(echo2) 
	file2.close()
	uploadFile("/tmp/{}_2.xml".format(uuid))

def search(term, location="palo alto ca", customerName=None, saveAs="file.csv"):
	params = {'term':term, 'location':location}
	log("Searching: {} in {}".format(term, location))
	#param_string = urllib.parse.urlencode(params)
	#conn = http.client.HTTPSConnection("api.yelp.com")
	#res = requests.get("https://api.yelp.com/v3/businesses/matches/best?", headers=headers, params=params)
	res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)

	#res = conn.getresponse()
	#data = res.read()
	#data = json.loads(data.decode("utf-8"))
	data = res.json()
	#input("CONTINUE")
	a = []
	# Iterate over all of the results for this search

	result = data["businesses"][0]
	name = result['name']
	location = result['location']["city"]
	phoneNum = result['display_phone']

	phoneScript = PHONE_CALL_SCRIPT.format(customerName, name, "November 18th", "3 pm")
	#print(len(results))
	alexaScript = "The closest match we could find was {} in {}".format(name, location)
	return phoneScript, alexaScript
		

def uploadFile(fileName):
	bucketID = tempBucketID
	finalFileName = fileName.replace("/tmp/", "")
	# This converts the bucketID from "https://s3.amazonaws.com/bucketid/" to "bucketid"
	finalFileName = finalFileName.split('/')[-1]
	# Converts the input from /whateverinput/ to whateverinput
	conn = tinys3.Connection(AMAZON_ACCESS_KEY,AMAZON_SECRET_KEY,tls=True)
	# This open up the s3 conneciton using the constants defined at the beginning
	# TODO - Ideally this would be a class that would take these vars on input and test...
	conn.upload(finalFileName, open(fileName,'rb'), bucketID)


def create_upload_text(restaraunt, location, name, personalPhone):
	uuid = gen_guid()
	text, alexaResponse = search(restaraunt, location, name)
	create_mp3(text, uuid)
	create_twiml(uuid, personalPhone)
	return alexaResponse, uuid


if __name__ == '__main__':
	# create_upload_text("veggie grille")
	text = """
	Thank you for confirming this reservation through BookMe!  
	We will contact the customer with a confirmation.  Goodbye.
	"""
	create_mp3(text, "ending")

######### This runs anytime echoLinguistics.py is imported  #######################
# createmp3List()
# This creates the list of mp3 files that have already been generated

#uploadFile("temp.txt")