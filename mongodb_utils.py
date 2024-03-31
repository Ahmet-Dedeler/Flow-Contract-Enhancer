from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDatabase:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        return collection.insert_one(document).inserted_id

    def find_document(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find_one(query)

    def find_documents(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find(query)

    def update_document(self, collection_name, query, new_values):
        collection = self.db[collection_name]
        return collection.update_one(query, {"$set": new_values})

    def delete_document(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.delete_one(query)