#!/usr/bin/env python3

import youtube_dl
import os
import sys
import time
import pymongo
from string import Template
import requests
from PIL import Image
import io
import subprocess
import re

CLIENT = pymongo.MongoClient()
DATABASE = CLIENT['video']
COLLECTION = DATABASE['videos']


APP_PATH = os.path.dirname(__file__)
sys.path.insert(0, APP_PATH)

VIDEO_DIR = os.path.join('/mnt', 'files', 'share', 'video/')


def add_paths_to_db(video_id, path, filename):
    COLLECTION.update_one({'_id': video_id}, {'$set': {'path': path}})
    COLLECTION.update_one({'_id': video_id}, 
            {'$set': {'filename': os.path.join(path, filename)}})


def video_folder_name(title):
    replace_chars = [' ', "'", '|', '?', '/', ':']
    re_comp = re.compile('[^A-Za-z0-9.]')
    return re_comp.sub('_', title)


def get_video(video_id, title):
    """
    Given an id, youtube-dl can will download
    the video.

    :param video_id: The unique video identifier 
    """
    path = os.path.join(VIDEO_DIR, video_folder_name(title))
    if os.path.exists(path) is False:
        os.mkdir(path)

    opts = {'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': os.path.join(VIDEO_DIR, video_folder_name(title), '%(title)s.%(ext)s'),
            'writesubtitles': False,
            'allsubtitles': False,
            'writethumbnail': False,
            'writedescription': False,
            'subtititleslang': 'en'}

    try:
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([video_id])
    except youtube_dl.utils.DownloadError:
        generic_video(video_id)

def generic_video(link):
    opts = {'outtmpl': VIDEO_DIR + '%(title)s.%(ext)s',
            'default_search': 'auto'}
            
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([link])

def write_nfo(video_id, title):
    i = COLLECTION.find_one({'_id': video_id})
    with open('./app/queue_processor/template.nfo', 'r') as fl:
        template = Template(fl.read())
    out_template = template.substitute(unique_id=i['_id'], studio=i['uploader'],
            title=i['title'], plot=i['description'],
            date_prem=i['upload_date'])
    path = os.path.join(VIDEO_DIR, video_folder_name(title), 'tvshow.nfo')
    with open(path, 'w') as fl:
        fl.write(out_template)


def mark_queue(video_id):
    COLLECTION.update_one({'_id': video_id}, {'$set': {'Processed': True}})


def get_thumbnail(url, title):
    data = requests.get(url, stream=True)
    image_data = Image.open(io.BytesIO(data.content))
    path = os.path.join(VIDEO_DIR, video_folder_name(title), 'thumbnail.jpg') 
    image_data.save(path, 'jpeg')


def process_queue():
    while True:
        #unprocessed = conn.execute('select id from queue where processed = 0')
        unprocessed = [i for i in COLLECTION.find({'Processed': False}, {'_id': True, 
            'title': True, 'thumbnail': True})]
        for i in unprocessed:
            get_video(i['_id'], i['title'])
            mark_queue(i['_id'])
            write_nfo(i['_id'], i['title'])
            get_thumbnail(i['thumbnail'], i['title'])

        time.sleep(10)


if __name__ == '__main__':
    process_queue()