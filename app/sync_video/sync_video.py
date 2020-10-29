#!/usr/bin/env python3
"""Web endpoints
"""


from __future__ import unicode_literals
from flask import Flask
from pymongo.errors import ConnectionFailure

from app.project_logging import logger
from app.video import VideoSearch
from app.sync_video.queue_manager import add_queue


app = Flask(__name__)


@app.route('/')
def index() -> str:
    """Return a generic page if site root explored

    Returns:
        str: generic string
    """
    return 'sync_video index'


@app.route('/Sync/<video_id>')
def sync_video(video_id: str) -> str:
    """Add video to database

    Args:
        video_id (str): id of video

    Returns:
        str: 'Invalid data' and error occurred
        str: '{video_id}' added
    """
    try:
        res = add_queue(video_id)
    except ConnectionFailure as e:
        logger.error(e)
        res = False

    if res is False:
        return 'Invalid data check log for error'
    else:
        return f'{video_id} added'


@app.route('/Sync/<video_id>/<tags>')
def sync_video_tags(video_id: str, tags: str) -> str:
    """Add video to database with tags

    Args:
        video_id (str): id of video
        tags (str): video tags separated by a comma
        e.g. /Sync/12345/some,fun,video

    Returns:
        str: empty string
    """

    res = False

    try:
        if tags.find(',') != -1:
            tag_list = [tag.lower() for tag in tags.split(',')]
            res = add_queue(video_id, tag_list)
        else:
            tags = [tags.lower()]
            res = add_queue(video_id, tags)
    except ConnectionFailure as e:
        logger.error(e)

    if res is False:
        return 'Invalid Data check log for error'
    else:
        return f'{video_id}, {tags} added'


@app.route('/delete/<video_id>')
def sync_delete_video(video_id: str) -> str:
    """delete a video from the database

    Args:
        video_id (str): the video_id

    Returns:
        str: '{video_id} has been removed from db'
        str: '{video_id} not found'
    """
    vid = VideoSearch.exact_find_video(_id=video_id)
    del_res = vid.delete_video(check=True)

    if del_res[0] == 0:
        res = f'{video_id} not found'
    elif del_res[0] == 1:
        res = f'{video_id} has been removed from db' \
                'however no path key was found in document' \
                'you will have to manually remove this'
    elif del_res[0] == 2:
        res = f'{video_id} has been removed from db' \
                '{del_res[1]} removed'
    else:
        res = 'unknown issues'

    return res
