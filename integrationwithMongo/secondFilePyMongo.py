import collections
import pprint
from http import client

import pymongo
import pymongo as pyM

cliente = pyM.MongoClient("mongodb+srv://codejacque:password@cluster0.xxtfhku.mongodb.net/?retryWrites=true&w=majority")
db = client.test
posts = db.posts

for post in posts.find():
    pprint.pprint(post)

print(posts.count_doments({}))
print(posts.count_documents({"author": "Mike"}))
print(posts.count_documents({"tags": "insert"}))

pprint.pprint(posts.find_one({"tags": "insert"}))

print("\nRecuperando info da coleção post de maneira ordenada")
for post in posts.find({}).sort("date"):
    pprint.pprint(post)

result = db.profiles.create_index([('auto', pymongo.ASCENDING)], unique=True)

print(sorted(list(db.profiles.index_information())))

user_profile_user = [
    {'user_id': 211, 'name': 'Luke'},
    {'user_id': 212, 'name': 'Joao' }]

result = db.profile.insert_many(user_profile_user)

print("\nColeções armazenadas no mongoDB")
print(db.list_collection_names())

# db['profiles'].drop()

for collection in collections:
    print(collection)

for post in posts.finf():
    pprint.pprint(post)

print(posts.delete_one({"author": "Mike"}))

