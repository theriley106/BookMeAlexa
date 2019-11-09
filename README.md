# BookMeAlexa
Amazon Alexa Skill to Book Restaurants 


-> User says restaraunt

-> Payload with restaraunt information gets sent to lambda function

-> Take restaraunt slot value and search for it somewhere

-> Grab phone number and restaraunt

-> Generate audio from information from payload -> Call with twilio and leave voicemail automatically

-> Function to make Amazon Polly mp3 of the specified message -> Sends to our backend to create a TWIML thing -> sends twiml url to twilio to make call

Create {uuid}.twiml and {uuid}.mp3 file and upload to s3 adn serve s3 file back

## Flow

