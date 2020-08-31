#!/usr/bin/env python3

#import sqlite3
import pymongo
from youtube_dl import YoutubeDL
from datetime import datetime

#conn = sqlite3.connect('/home/ubuntu/code/video/video_db/queue.db', check_same_thread=False)
info_extractor = YoutubeDL(params={'simulate': True})
client = pymongo.MongoClient()
database = client['video']
collection = database['videos']

def get_video_info(video_id):
    #info_keys = ['uploader', 'upload_date', 'description']
    video_info = info_extractor.extract_info(video_id)
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
    result = [i['_id'] for i in collection.find({'_id': video_id})]

    if result == []:
        return False
    else:
        return True

def add_queue(video_id):
    if check_db(video_id) is True:
        return None

    collection.insert_one(get_video_info(video_id))
   # with conn:
   #     conn.execute('insert into queue values (?,?)', (video_id,0,))
