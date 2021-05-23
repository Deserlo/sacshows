from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
import sys
import os
import datetime
from datetime import timezone
from dotenv import load_dotenv
load_dotenv()
import shortuuid
import pprint
import json
import re


MONGO_URI = os.getenv("MONGO_URI")
#app.config["MONGO_URI"] = MONGO_URI






class Mongo(object):

    def __init__(self, mongo_uri):
        self.connection_string = mongo_uri
        self.client = MongoClient(self.connection_string).Sactown.Events
    


    def find(self, query):
        '''
        Finds all documents
        '''
        cursor = self.client.find(query)
        list_cur = list(cursor)
        json_docs = dumps(list_cur)
        return list_cur


    def update_all(self, query, val):
        #db.articles.update({},{$set: {"published":true}},false,true)
        self.client.update_many(query,{"$set": { "venue": val } }, False, array_filters=None)
    
    def update_one(self, oid, val):
        self.client.update_one({"_id": oid},{"$set": { "youtube id": val}})





'''
MongoDB = Mongo(MONGO_URI)
cursor = MongoDB.find()
for c in cursor:
    #sh_uid = shortuuid.uuid()[:11]
    oid = c['_id']
    #print(sh_uid)
    print(oid)
    #MongoDB.update_one(oid, sh_uid)


            {"_id" : ObjectId("5cfbb46d6fb0f3245fd8fd34")},
    {"$set":
        {"some field": "OBJECTROCKET ROCKS!!"}
    },upsert=True
'''

def clean_venue_names():
    MongoDB = Mongo(MONGO_URI)
    rgx = re.compile('.*ettore.*', re.IGNORECASE)
    query = {"venue": rgx}
    val = "ettore's bakery and restaurant"
    MongoDB.update_all(query, val.lower())
    cursor = MongoDB.find(query)
    for c in cursor:
        ps = c['performers']
        print(ps)


def insert_new_key():
    MongoDB = Mongo(MONGO_URI)
    query = {"venue": "powerhouse pub (folsom)"}
    cursor = MongoDB.find(query)
    for c in cursor:
        oid = c['_id']
        perfs = c['performers']
        print(perfs)
        vals = ""
        MongoDB.update_one(oid,vals)


#creating uids
def create_uids():
    for i in range(50):
        s = shortuuid.uuid()[:11]
        print(s)


def get_venue_names():
    MongoDB = Mongo(MONGO_URI)
    cursor = MongoDB.find({})
    list_cur = list(cursor)
    new_list = []
    for v in list_cur:
        new_list.append(v['venue'])
    my_set = set(new_list)
    for s in my_set:
        print(s)



if __name__ == '__main__':
    clean_venue_names()
    

