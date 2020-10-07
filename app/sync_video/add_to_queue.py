#!/usr/bin/env python3
"""
Add unprocessed items to the database
"""

import sys
import os
from youtube_dl import YoutubeDL
from datetime import datetime

APP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_PATH)

import app.config as cfg
from app.database import COLLECTION

INFO_EXTRACTOR = YoutubeDL(params=cfg.SYNC_YOUTUBE_DL_PARAMS)


def get_video_info(video_id, tags=None):
    """
    Call the method youtube_dl.YoutubeDL.extract_info,
    then create a dictionary object including any optional
    tags. The returned dictionary object is what get's
    inserted into the database (note this method does
    not actually insert data, only produce it)

    Args:
        video_id (str): The id of a youtube video
        tags (list(str)) _optional_: A list of tags

    Returns:
        A dictionary

        {'_id': 'video_id',
        'Processed': False,
        'title': 'video title',
        'uploader': 'video creator',
        'upload_date': 'video upload date (%Y%m%d)'
        'description': 'video description',
        'thumbnail': 'video thumbnail (url)',
        'tags': [tags]}


    """
    if tags is None:
        tags = []

    video_info = INFO_EXTRACTOR.extract_info(video_id)
    info = {
        '_id': video_info['id'],
        'Processed': False,
        'title': video_info['title'],
        'uploader': video_info['uploader'],
        'upload_date': datetime.strptime(video_info['upload_date'], '%Y%m%d'),
        'description': video_info['description'],
        'thumbnail': video_info['thumbnail'],
        'tags': tags}

    return info

def check_db(video_id):
    """
    Query the database and assert if the value exists.

    Args:
        video_id (str): The id of a youtube video

    Returns:
        False if video does not exist
        True if video does exist
    """
    result = [i['_id'] for i in COLLECTION.find({'_id': video_id})]

    if result == []:
        return False
    else:
        return True

def add_queue(video_id, tags=None):
    """
    If the video_id does not exist, insert
    an entry into the database from the information
    provided by get_video_info

    Args:
        video_id (str): The id of a youtube video
        tags (list(str)) _optional_: A list of tags
    Returns:
        None
    """

    if check_db(video_id) is True:
        pass

    COLLECTION.insert_one(get_video_info(video_id, tags))
