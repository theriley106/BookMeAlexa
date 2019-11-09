import pymongo
import json
from bson.json_util import dumps
from keys import *

client = pymongo.MongoClient(MONGO_STRING)
print client.list_database_names()

db = client.blog

def add():
	db.posts.insert_one({"AYY": "THIS WORKS"})

def read():
	for post in client.blog.posts.find():
		print(post)

if __name__ == '__main__':
	print read()