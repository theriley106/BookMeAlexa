#!/usr/bin/python

import boto3
from contextlib import closing
from keys import *

ACCESS_KEY = POLLY_KEY

SECRET_KEY = POLLY_SECRET



client = boto3.client('polly',aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,region_name='us-east-2')

response = client.synthesize_speech(
    OutputFormat='mp3',
    Text='Amazon Polly is a service that turns text into lifelike speech. Polly lets you create applications that talk, enabling you to build entirely new categories of speech-enabled products. Polly is an Amazon AI service that uses advanced deep learning technologies to synthesize speech that sounds like a human voice. Polly includes 47 lifelike voices spread across 24 languages, so you can select the ideal voice and build speech-enabled applications that work in many different countries.',
    TextType='text',
    VoiceId='Salli'
)

print response

if "AudioStream" in response:
    with closing(response["AudioStream"]) as stream:
        output = "polly-boto.mp3"

        try:
            # Open a file for writing the output as a binary stream
            with open(output, "wb") as file:
                file.write(stream.read())
        except IOError as error:
            # Could not write to file, exit gracefully
            print(error)
            sys.exit(-1)