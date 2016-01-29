#!/usr/bin/env python3

import json
import os
from pymongo import MongoClient
import re

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client['tweets']
collection= db['rawTweets']
os.chdir("/home/neeraj/Downloads/twitterstream-to-mongodb/Transfer/")
fileslist = os.listdir(".")
files = filter(os.path.isfile,fileslist)
for fl in files:
    json_data=open(fl)
    jayson=json_data.readlines()
    for jason in jayson:
        d=json.loads(jason)
        k= { "text": d["text"],  "retweets": d["retweet_count"] , "favorites" : d["favorite_count"], "name" : d["user"]["name"],"followers" : d["user"]["followers_count"],"screen_name" : d["user"]["screen_name"] , "date" : d["created_at"] }
        collection.insert_one(k)
    os.rename(fl , "InDB/"+fl)
