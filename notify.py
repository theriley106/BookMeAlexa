import requests
import datetime
from keys import *

NOTIFY_KEY = "Atc|MQEBICeNIsdEH73qGlysndjQXxmWhGVumLGyBOtaFK7Z047cAWi5m76fb9a3eHG91iNII70kW7Zjs3NN98KD59fMk4u0BIpxU8CmxqE3o6HbvzvTl336XjFHqkgERCxNJJRCdhcpKXlK4W1ptxTYCOdiwGFI0NT41r0j3QCQySj2JOWOfEne2z-1DZma-NqpVzI41lOiuQLEGBwLJfqjWFo97Wn_7lDDTY2teR1ORRNb4IeVjZ3IVZPFujV9HDVa8Nba0MIbM5p4KaHV777mGrDINBTUHWVdk_7qUdRVv7Zc9RSnJw"

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

if __name__ == '__main__':

	currentTime = datetime.datetime.now()
	userID = "amzn1.ask.account.AHJ7DE73A6ZMOIMPCTB5J62JNL7Q3ZCSXBDPM7BDLIGNICMUQY2BJYATHMKH5QLPIW5LYF32QUHDZ7MGM3Q276BVO37OUFY5ZC5KF6BENYNVJSL4KNVM6BISUO3ULRCW3FNX7RRFT4WBWXVSQJM7NKYKJU7D3VUNW5PO6EFNJEEOO42JS4YK224Z6OIGSADIB577ZHCJY73DTJY"
	token = NOTIFY_KEY
	data = {
	    "timestamp": get_timestamp(currentTime),
	    "referenceId": "new-instae",
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