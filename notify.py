import requests
import datetime
from keys import *

def get_timestamp(currentTime, addVal=0):
	a = "{0}.00Z"
	timeNow = currentTime + datetime.timedelta(addVal, 0)
	return a.format(timeNow.replace(microsecond=0).isoformat())

def send_notification(userID):
	currentTime = datetime.datetime.now()
	headers = {
	    'Content-Type': 'application/x-www-form-urlencoded',
	}

	data = {
	  'grant_type': 'client_credentials',
	  'client_id': ALEXA_CLIENT_ID,
	  'client_secret': ALEXA_CLIENT_SECRET,
	  'scope': 'alexa::proactive_events'
	}

	response = requests.post('https://api.amazon.com/auth/o2/token', headers=headers, data=data)
	response = response.json()
	print("AUTH FLOW")
	print(response)
	token = response['access_token']

	data = {
	    "timestamp": get_timestamp(currentTime),
	    "referenceId": "unique-id-of-this-instance",
	    "expiryTime": get_timestamp(currentTime, 1),
	    "event": {
		    "name": "AMAZON.OrderStatus.Updated",
		    "payload": {
		      "state": {
		        "status": "PREORDER_RECEIVED"
		      },
		      "order": {
		        "seller": {
		          "name": "BookMe"
		        }
		      }
		    }
		  },
	    "localizedAttributes": [
	    {
	      "locale": "en-US",
	      "sellerName": "Amazon"
	    }],
	    "relevantAudience": {
	        "type": "Unicast",
	        "payload": {
	            "user": userID
	        }
	    }
	}

	"https://api.amazonalexa.com/v1/proactiveEvents/"
	headers = {
	    "Content-Type": "application/json",
	    "Authorization": "Bearer " + token
	}
	response = requests.post('https://api.amazonalexa.com/v1/proactiveEvents/', headers=headers, json=data)
	print("RESPONSE FROM NOTIFICATION")
	print(response.text)