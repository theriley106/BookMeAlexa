import responses
import echo
import requests
import re
from keys import *
import db
import notify


DEFAULT_LOCATION = "Greenville SC"

def send_text(body, number=5305485102):
	print("SENDING TEXT")
	number = str(number)
	headers = {
		'Authorization': 'Bearer {}'.format(STD_KEY),
	}

	data = {
	  'to': number,
	  'body': body
	}

	response = requests.post('https://utils.api.stdlib.com/sms@1.0.11/', headers=headers, data=data)
	print response.text
	
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

def convert_time(value):
	minutes = 0
	if ':' in str(value):
		value, minutes = value.split(":")
	partOfDay = " AM"
	if int(value) > 12:
		partOfDay = " PM"
		value = int(value) - 12
	timeVal = str(value)
	if int(minutes) > 0:
		timeVal += " {}".format(minutes)
	timeVal += partOfDay
	return timeVal

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

def on_intent(intent_request, session, location, name, personalPhone, dateVal, timeVal):
	print(intent_request)
	# This means the person asked the skill to do an action
	intent_name = intent_request["intent"]["name"]
	# This is the name of the intent (Defined in the Alexa Skill Kit)
	if intent_name == 'whatDay':
		# whatDay intent
		return responses.what_day(), None, None
		# Return the response for what day
	elif intent_name == 'pleaseBook':
		restaraunt = intent_request["intent"]["slots"]["restaraunt"]["value"]
		return echo.create_upload_text(restaraunt, location, name, personalPhone, dateVal, convert_time(timeVal))
	elif intent_name == 'whatBuy':
		return responses.what_can_i_buy(), None, None

def get_product_response(event, context):
	headers = {
		'Content-type': 'application/json',
		'Accept-Language': 'en-US',
		'Authorization': 'Bearer {}'.format(event['context']['System']['apiAccessToken']),
	}

	response = requests.get('https://api.amazonalexa.com/v1/users/~current/skills/~current/inSkillProducts', headers=headers)
	return response.json()
		
def lambda_handler(event, context):
	purchaseID = None
	print("event")
	print(event)
	print("context")
	print(context)

	
	userID = event['session']['user']['userId']

	name = extract_name(event, context)
	location = extract_lat_long(event, context)
	phoneNumber = extract_phone(event, context)
	# This is the user phone number
	productResponse = get_product_response(event, context)
	endSession = True
	if event["request"]["type"] == "LaunchRequest":
		speech = responses.start_response()
		endSession = False
	elif event["request"]["type"] == "IntentRequest":

		if event["request"]["intent"]["name"] == 'whatBuy':
			speech = responses.what_can_i_buy()
		else:
			isPurchased = productResponse['inSkillProducts'][0]['entitlementReason'] == 'PURCHASED'

			if isPurchased and db.get_user(userID) != None:
				restaraunt = event["request"]["intent"]["slots"]["restaraunt"]["value"]
				speech, uuid, restaurantNumber = on_intent(event["request"], event["session"], location, name, phoneNumber)
				db.add(userID, restaraunt, location, uuid, restaurantNumber)
				echo.make_call(restaurantNumber, db.get_user(userID)['uuid'])
				db.delete(userID)


			else:
				purchaseID = productResponse['inSkillProducts'][0]['productId']
				restaraunt = event["request"]["intent"]["slots"]["restaraunt"]["value"]
				dateVal = event["request"]["intent"]["slots"]["dateVal"]["value"]
				timeVal = event["request"]["intent"]["slots"]["timeVal"]["value"]
				speech, uuid, restaurantNumber = on_intent(event["request"], event["session"], location, name, phoneNumber, dateVal, timeVal)
				db.add(userID, restaraunt, location, uuid, restaurantNumber)
	else:
		echo.make_call(db.get_user(userID)['restaurant_number'], db.get_user(userID)['uuid'])
		# echo.make_call(RESTAURANT_PHONE_NUMBER, db.get_user(userID)['uuid'])
		db.delete(userID)
		speech = "We will let you know after the reservation has been made"
		send_text("Reservation has been successfully placed for {}".format(name))
	x = returnSpeech(speech, product=purchaseID, endSession=endSession)
	print(x)
	return x

if __name__ == '__main__':
	pass
