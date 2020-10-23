#!/usr/bin/env python3
"""Connection to database
"""
import pymongo
from app.config import DBConfig as cfg

CLIENT = pymongo.MongoClient(cfg.mongo_server)
DATABASE = CLIENT[cfg.mongo_database]
COLLECTION = DATABASE[cfg.mongo_collection]
