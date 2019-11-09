import pymongo
import json
from bson.json_util import dumps
from keys import *

client = pymongo.MongoClient(MONGO_STRING)
print client.list_database_names()

db = client.blog

def add(userID, query, location, uuid):
	client.blog.posts.insert_one({"user": userID, "query": query, 'location': location, "uuid": uuid})

def read():
	for post in client.blog.posts.find():
		print(post)

def get_user(userID):
	return client.blog.posts.find_one({"user": userID})

def delete(userID):
	client.blog.posts.delete_many({"user": userID})

def update():
	myquery = { "blog": "sample_airbnb" }
	newvalues = { "$set": { "blog": "updated_sample_airbnb" } }

	client.blog.posts.update_one(myquery, newvalues)

if __name__ == '__main__':
	add('chris', 'subway', 'palo alto', '12345')

	print("\n\nOLD\n\n")
	read()
	print("\n\nNEW\n\n")
	read()
	print get_user('chris')