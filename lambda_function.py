import responses
import echo
import requests
import re
from keys import *

DEFAULT_LOCATION = "Greenville SC"

def returnSpeech(speech, endSession=True, product=None):
	a = {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			"outputSpeech": {
			"type": "PlainText",
			"text": speech
				},
			"shouldEndSession": endSession

		}
	}

	if product != None:
		a['response']["directives"] = [
			    {
			      "type": "Connections.SendRequest",
			      "name": "Buy",
			      "payload": {
			        "InSkillProduct": {
			          "productId": product
			        }
			      },
			      "token": "correlationToken"
			    }
			  ]

	return a

def extract_lat_long(event, context):
	try:
		try:
			deviceID = event["context"]["System"]['device']['deviceId']
		except:
			deviceID = "Test"
		try:
			key = event["context"]["System"]['apiAccessToken']
		except:
			key = ""
			deviceID = "Test"
		# This returns a dictionary object
		headers = {'Host': 'api.amazonalexa.com', 'Accept': 'application/json', 'Authorization': "Bearer {}".format(key)}
		url = 'https://api.amazonalexa.com/v1/devices/{}/settings/address'.format(deviceID)
		res = requests.get(url, headers=headers).json()
		returnVal = res["city"] + " " + res['stateOrRegion']
	except:
		returnVal = DEFAULT_LOCATION
	return returnVal

def extract_name(event, context):
	try:
		try:
			deviceID = event["context"]["System"]['device']['deviceId']
		except:
			deviceID = "Test"
		try:
			key = event["context"]["System"]['apiAccessToken']
		except:
			key = ""
			deviceID = "Test"
		# This returns a dictionary object
		headers = {'Host': 'api.amazonalexa.com', 'Accept': 'application/json', 'Authorization': "Bearer {}".format(key)}
		url = "https://api.amazonalexa.com/v2/accounts/~current/settings/Profile.name"
		name = requests.get(url, headers=headers).text
		returnVal = name
	except:
		returnVal = DEFAULT_NAME
	return returnVal.replace('"', '')

def extract_phone(event, context):
	try:
		try:
			deviceID = event["context"]["System"]['device']['deviceId']
		except:
			deviceID = "Test"
		try:
			key = event["context"]["System"]['apiAccessToken']
		except:
			key = ""
			deviceID = "Test"
		# This returns a dictionary object
		headers = {'Host': 'api.amazonalexa.com', 'Accept': 'application/json', 'Authorization': "Bearer {}".format(key)}
		url = "https://api.amazonalexa.com/v2/accounts/~current/settings/Profile.name"
		phoneNum = requests.get(url, headers=headers).json()
		returnVal = phoneNum["phoneNumber"]
	except:
		returnVal = DEFAULT_NUMBER
	return returnVal.replace("-", "")

def on_intent(intent_request, session, location, name):
	print(intent_request)
	# This means the person asked the skill to do an action
	intent_name = intent_request["intent"]["name"]
	# This is the name of the intent (Defined in the Alexa Skill Kit)
	if intent_name == 'whatDay':
		# whatDay intent
		return responses.what_day(), None
		# Return the response for what day
	elif intent_name == 'pleaseBook':
		restaraunt = intent_request["intent"]["slots"]["restaraunt"]["value"]
		return echo.create_upload_text(restaraunt, location, name)
		
def lambda_handler(event, context):
	purchaseID = None
	userID = event['session']['user']['userId']
	if event["request"]["type"] == "LaunchRequest":
		speech = responses.start_response()
	elif event["request"]["type"] == "IntentRequest":

		import db
		headers = {
		    'Content-type': 'application/json',
		    'Accept-Language': 'en-US',
		    'Authorization': 'Bearer {}'.format(event['context']['System']['apiAccessToken']),
		}

		response = requests.get('https://api.amazonalexa.com/v1/users/~current/skills/~current/inSkillProducts', headers=headers)
		print("event")
		print(event)
		print("context")
		print(context)
		productResponse = response.json()
		name = extract_name(event, context)
		print("NAME: {}".format(name))
		print(productResponse)
		location = extract_lat_long(event, context)
		purchaseID = productResponse['inSkillProducts'][0]['productId']
		restaraunt = event["request"]["intent"]["slots"]["restaraunt"]["value"]
		speech, uuid = on_intent(event["request"], event["session"], location, name)
		db.add(userID, restaraunt, location, uuid)
	else:

		import db
		print("event")
		print(event)
		print("context")
		print(context)
		speech = "AYY THIS WORKED I THINK"
		phoneNumber = extract_phone(event, context)
		print("PHONE NUMBER: {}".format(phoneNumber))
		echo.make_call("8645674106", db.get_user(userID)['uuid'])
		db.delete(userID)
		speech = "We will let you know after the reservation has been made"
	x = returnSpeech(speech, product=purchaseID)
	print(x)
	return x

if __name__ == '__main__':
	pass
