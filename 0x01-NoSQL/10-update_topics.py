#!/usr/bin/env python3
""" 10-main """

def update_topics(mongo_collection, name, topics):
    """Inserts a new document in a collection"""
    return mongo_collection.insert_one(kwargs).inserted_id

from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
school_collection = client.my_db.school
new_school_id = insert_school(school_collection, name="UCSF", address="505 Parnassus Ave")
print("New school created: {}".format(new_school_id))
