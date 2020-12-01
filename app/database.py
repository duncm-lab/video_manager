#!/usr/bin/env python3
"""Connection to database
"""
import pymongo
from app.config_loader import load_config

mongo_server = load_config('mongo_db')['mongo_server']
db = load_config('mongo_db')['mongo_database']
col = load_config('mongo_db')['mongo_collection']

CLIENT = pymongo.MongoClient(mongo_server)

if db not in CLIENT.list_database_names():
    newdb = CLIENT[db]
    newdb.create_collection(col)


DATABASE = CLIENT[db]
COLLECTION = DATABASE[col]
