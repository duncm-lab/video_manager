#!/usr/bin/env python3
"""
Read the document tags in the database and create folders
based on those tags if they do not exist
"""

import os
import sys
import pymongo
from string import Template


from app import config as cfg
from app.config import BASE_PATH

CLIENT = pymongo.MongoClient(cfg.MONGO_SERVER)
DATABASE = CLIENT[cfg.MONGO_DATABASE]
COLLECTION = DATABASE[cfg.MONGO_COLLECTION]

tagged = [(i['tags']) for i in COLLECTION.find() if 'tags' in i.keys()]

flat = []

for i in tagged:
    if type(i) == list:
        for j in i:
            flat.append(j)
    else:
        flat.append(i)

folders = tuple(set(flat))

def create_path(folder):
    if not os.path.exists(BASE_PATH + folder):
        os.mkdir(BASE_PATH + folder)

for i in folders:
    create_path(i)
