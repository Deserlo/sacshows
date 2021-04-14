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

#MONGO_URI = os.getenv("MONGO_URI")
#app.config["MONGO_URI"] = MONGO_URI






class Mongo(object):

    def __init__(self, mongo_uri):
        self.connection_string = mongo_uri
        self.client = MongoClient(self.connection_string).Sactown.Events
    

    def find(self):
        '''
        Finds all documents
        '''
        cursor = self.client.find({})
        list_cur = list(cursor)
        json_docs = dumps(list_cur)
        return list_cur


    def update_all(self):
        #db.articles.update({},{$set: {"published":true}},false,true)
        self.client.update_many({},{"$set": { "uuid": shortuuid.uuid() } }, False, array_filters=None)

    def update_one(self, oid, sh_uid ):
        self.client.update_one({"_id": oid},{"$set": { "uuid": sh_uid}})



'''
MongoDB = Mongo(MONGO_URI)
cursor = MongoDB.find()
for c in cursor:
    sh_uid = shortuuid.uuid()[:11]
    oid = c['_id']
    print(sh_uid)
    print(oid)
    MongoDB.update_one(oid, sh_uid)


            {"_id" : ObjectId("5cfbb46d6fb0f3245fd8fd34")},
    {"$set":
        {"some field": "OBJECTROCKET ROCKS!!"}
    },upsert=True
'''

for i in range(25):
    s = shortuuid.uuid()[:11]
    print(s)


#s = shortuuid.uuid()[:11]
#print(s)
    

