<h1 align="center"><a href="https://www.youtube.com/watch?v=oCiOAlz5b8w">Watch the Video Demo</a></h1>

## What it does

**Book Me enables users to book reservations at *any* local restaurant using their Amazon Alexa by placing an automated phone call on their behalf.**

![user flow](https://raw.githubusercontent.com/theriley106/BookMeAlexa/master/static/image1.png?token=AE5MVIN4ME5PAMUIYCZTJQC52QVZC)

## Technical Details

The request is sent to our **Lambda function**.  "Olive Garden", "November 18th" and "8:30PM" are extracted, and we pull the user's contact information and geographical location through the `api.amazonalexa.com` endpoint.

Information about the user and the reservation request is saved in a **MongoDB database**, and the restaurant name and user location is passed into the **Yelp Fusion API** to return nearby restaurants that match the search query.

The user is prompted for an in-skill purchase to book the reservation (given a match is found), and after a successful payment we generate an audio file using the **Amazon Polly** text-to-speech service based on the following call template:

```
This is an automated message from Book Me powered by the Alexa voice service.  
Press pound to hear the message now.

I am calling on behalf of {user's full name} who has 
requested a reservation at {restaurant name} on {date} at {time}.

Press the pound sign to confirm this reservation, 
or 2 to be forwarded to the customer.
```

After the audio is generated, we host the mp3 in an **S3 bucket** and generate a **[TwiML flow](https://www.twilio.com/docs/voice/twiml)** to handle the call interaction.

A call is then placed to the restaurant using **Twilio**.  You can hear an [example call here](https://youtu.be/oCiOAlz5b8w?t=62).

## [I can handle] the Business Side

Using Twilio for handling the call interaction is extremely inexpensive.  

Twilio charges **$0.0130/min** for domestic calls, and our maximum call length is **62 seconds** assuming the call was not transferred to the customer.

Amazon Polly charges $4.00 for every million characters of speech generated.  The speech generated in an automated Book Me call depends on the length of the restaurant and customer name, but it should always fall between **300-400 characters**.  Certain parts of the message can be generated a single time and reused, which can cut down the costs significantly.

Amazon S3 costs are negligible given the size of the files being hosted, but the standard rate is **$0.023 per GB**.  A full audio file and TwiML file is roughly ~1.1mb.

Our costs:

- Amazon Polly: $0.0012/call
- Twilio: $0.0134/call
- S3: $0.000023/call

This means that our total cost per call is **$0.014623** or less than 2 cents per call.

- Consumable Price: **$0.99**
- Amazon Fee (30%): **~$0.30**
- Our Costs: **~$0.02**

Total Profit: **~$0.67/call**

<h1 align="center"><a href="https://devpost.com/software/book-me-ro24lj">View the Devpost Project</a></h1>
