#!/usr/bin/env python3
"""Connection to database
"""
import pymongo
from app.config import DBConfig as cfg

CLIENT = pymongo.MongoClient(cfg.mongo_server)

if 'video' not in CLIENT.list_database_names():
    newdb = CLIENT[cfg.mongo_database]
    newdb.create_collection(cfg.mongo_collection)


DATABASE = CLIENT[cfg.mongo_database]
COLLECTION = DATABASE[cfg.mongo_collection]
