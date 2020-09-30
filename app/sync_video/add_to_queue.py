#!/usr/bin/env python3

#import sqlite3
import sys
import os
import pymongo
from youtube_dl import YoutubeDL
from datetime import datetime

APP_PATH = os.path.dirname(__file__)
sys.path.insert(0, APP_PATH)

#conn = sqlite3.connect('/home/ubuntu/code/video/video_db/queue.db', check_same_thread=False)
INFO_EXTRACTOR = YoutubeDL(params={'simulate': True})
CLIENT = pymongo.MongoClient('mongodb://localhost:27017')
DATABASE = CLIENT['video']
COLLECTION = DATABASE['videos']

def get_video_info(video_id):
    #info_keys = ['uploader', 'upload_date', 'description']
    video_info = INFO_EXTRACTOR.extract_info(video_id)
    info = {
        '_id': video_info['id'],
        'Processed': False,
        'title': video_info['title'],
        'uploader': video_info['uploader'],
        'upload_date': datetime.strptime(video_info['upload_date'],
            '%Y%m%d'),
        'description': video_info['description'],
        'thumbnail': video_info['thumbnail']}

    return info

def check_db(video_id):
#    with conn:
#        v = conn.execute("select id from queue where id = ?", (video_id,))
#
#    result = v.fetchone()
    result = [i['_id'] for i in COLLECTION.find({'_id': video_id})]

    if result == []:
        return False
    else:
        return True

def add_queue(video_id):
    if check_db(video_id) is True:
        return None

    COLLECTION.insert_one(get_video_info(video_id))
   # with conn:
   #     conn.execute('insert into queue values (?,?)', (video_id,0,))
