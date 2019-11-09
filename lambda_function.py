import responses
import echo

def returnSpeech(speech, endSession=True):
	return {
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

def on_intent(intent_request, session):
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
		return echo.create_upload_text(restaraunt)
		
def lambda_handler(event, context):
	if event["request"]["type"] == "LaunchRequest":
		speech = responses.start_response()
	elif event["request"]["type"] == "IntentRequest":
		speech = on_intent(event["request"], event["session"])
	return returnSpeech(speech)

if __name__ == '__main__':
	pass
