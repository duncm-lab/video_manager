#!/usr/bin/env python3
"""Web endpoints
"""


from __future__ import unicode_literals
import sys
import os
from flask import Flask
from pymongo.errors import ConnectionFailure

APP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_PATH)
sys.path.insert(0, os.getcwd())

from app.project_logging import logger # pylint: disable=wrong-import-position
from app.sync_video.add_to_queue import add_queue # pylint: disable=wrong-import-position


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
        str: empty string
    """
    try:
        add_queue(video_id)
    except ConnectionFailure as e:
        logger.error(e)
    return ''

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
    try:
        if tags.find(',') != -1:
            tag_list = [tag.lower() for tag in tags.split(',')]
            add_queue(video_id, tag_list)
        else:
            tags = tags.lower()
            add_queue(video_id, tags)
    except ConnectionFailure as e:
        logger.error(e)
    return ''
