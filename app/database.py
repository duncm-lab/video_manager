#!/usr/bin/env python3
"""
Connection to database
"""
import pymongo
import config as cfg 

CLIENT = pymongo.MongoClient(cfg.MONGO_SERVER)
DATABASE = CLIENT[cfg.MONGO_DATABASE]
COLLECTION = DATABASE[cfs.MONGO_COLLECTION]
