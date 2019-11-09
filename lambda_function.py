import responses
import echo
import requests

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

def on_intent(intent_request, session, location):
	print(intent_request)
	# This means the person asked the skill to do an action
	intent_name = intent_request["intent"]["name"]
	# This is the name of the intent (Defined in the Alexa Skill Kit)
	if intent_name == 'whatDay':
		# whatDay intent
		return responses.what_day()
		# Return the response for what day
	elif intent_name == 'pleaseBook':
		restaraunt = intent_request["intent"]["slots"]["restaraunt"]["value"]
		return echo.create_upload_text(restaraunt, location)
		
def lambda_handler(event, context):
	purchaseID = None
	if event["request"]["type"] == "LaunchRequest":
		speech = responses.start_response()
	elif event["request"]["type"] == "IntentRequest":
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
		print(productResponse)
		location = extract_lat_long(event, context)
		purchaseID = productResponse['inSkillProducts'][0]['productId']
		speech = on_intent(event["request"], event["session"], location)
	else:
		print("event")
		print(event)
		print("context")
		print(context)
		speech = "AYY THIS WORKED I THINK"
	x = returnSpeech(speech, product=purchaseID)
	print(x)
	return x

if __name__ == '__main__':
	pass
