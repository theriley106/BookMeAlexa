def start_response():
	# This is the speech that is said when the skill starts for the first time
	return """Thank you for checking out Book Me.  An Amazon Alexa skill that can 
	book reservations at any local restaurant -- even those without online booking systems.
	"""

def what_can_i_buy():
	return """Book me will make a phone call to the restaurant on your behalf -- this is a premium service
	that costs 99 cents"""

def what_day():
	# This is the speech that is said when the person asks what day the event starts
	return "Hello world will take place on October 10th"
