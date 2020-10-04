#!/usr/bin/env python3

#import sqlite3
import sys
import os
from youtube_dl import YoutubeDL
from datetime import datetime

APP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_PATH)

from app.database import COLLECTION

import app.config as cfg

INFO_EXTRACTOR = YoutubeDL(params=cfg.SYNC_YOUTUBE_DL_PARAMS)

def get_video_info(video_id, tags=[]):
    video_info = INFO_EXTRACTOR.extract_info(video_id)
    info = {
        '_id': video_info['id'],
        'Processed': False,
        'title': video_info['title'],
        'uploader': video_info['uploader'],
        'upload_date': datetime.strptime(video_info['upload_date'],
            '%Y%m%d'),
        'description': video_info['description'],
        'thumbnail': video_info['thumbnail'],
        'tags': tags}

    return info

def check_db(video_id):
    result = [i['_id'] for i in COLLECTION.find({'_id': video_id})]

    if result == []:
        return False
    else:
        return True

def add_queue(video_id, tags=[]):
    if check_db(video_id) is True:
        return None

    COLLECTION.insert_one(get_video_info(video_id, tags))
