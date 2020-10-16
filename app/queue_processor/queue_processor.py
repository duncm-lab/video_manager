#!/usr/bin/env python3
"""
Download and process videos with youtube_dl
"""

import youtube_dl
import os
import sys
import time
from string import Template
import requests
from PIL import Image
import io
import re
import logging

APP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_PATH)
sys.path.insert(0, os.getcwd())

import app.config as cfg # pylint: disable=wrong-import-position
from app.database import COLLECTION # pylint: disable=wrong-import-position
from app.config import VIDEO_DIR # pylint: disable=wrong-import-position
from app.config import PROCESS_YOUTUBE_DL_PARAMS # pylint: disable=wrong-import-position

#create a local log file if we can't find the one defined in the config
log_path_check = os.path.abspath(os.path.dirname(cfg.QUEUE_PROCESSOR_LOG))

if not os.path.exists(log_path_check):
    log_file = 'queue_processor.log'
else:
    log_file = cfg.QUEUE_PROCESSOR_LOG

logging.basicConfig(filename=log_file, level=getattr(logging, cfg.LOG_LEVEL))
logger = logging.getLogger()



def video_folder_name(title):
    """
    Sanitize the folder name of invalid posixpath characters

    Args:
        title (str): name to be sanitized

    Returns:
        (str) sanitized folder name
    """
    re_comp0 = re.compile('[^A-Za-z0-9.]')
    re_comp1 = re.compile('_{2,}')
    return re_comp1.sub('_', re_comp0.sub('_', title))


def get_video(video_id, title):
    """
    Given an id, youtube-dl can will download
    the video.

    Args:
        video_id (str): id of youtube video
        title (str): title of video

    Returns:
        None
    """

    path = os.path.join(VIDEO_DIR, video_folder_name(title))
    if os.path.exists(path) is False:
        os.mkdir(path)

    output_folder = os.path.join(path, video_folder_name(title))
    opts = PROCESS_YOUTUBE_DL_PARAMS
    opts['outtmpl'] = output_folder
    opts['logger'] = logger


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
    try:
        with open(os.path.join(APP_PATH, 'template.nfo'), 'r') as fl:
            template = Template(fl.read())
    except FileNotFoundError as e:
        logger.error(e)

    out_template = template.substitute(unique_id=i['_id'], studio=i['uploader'], \
            title=i['title'], plot=i['description'], \
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
        unprocessed = COLLECTION.find({'Processed': False}, {'_id': True, \
            'title': True, 'thumbnail': True})
        for i in unprocessed:
            get_video(i['_id'], i['title'])
            mark_queue(i['_id'])
            write_nfo(i['_id'], i['title'])
            get_thumbnail(i['thumbnail'], i['title'])


        time.sleep(10)


if __name__ == '__main__':
    process_queue()
