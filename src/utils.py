from pymongo import MongoClient

client = MongoClient()
db = client['project2']
collection = db['file_uploads']

for doc in collection.find():
    print(doc)
