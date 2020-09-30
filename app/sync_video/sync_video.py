#!/usr/bin/env python3
from __future__ import unicode_literals
import sys
import os
import logging
from flask import Flask

APP_PATH = os.path.dirname(__file__)
sys.path.insert(0, APP_PATH)

from add_to_queue import add_queue

logging.basicConfig(filename = '/sync_video_logs/sync_video.log',
        level = logging.DEBUG)

logger = logging.getLogger()

app = Flask(__name__)

@app.route('/')
def index():
    return 'sync_video index'

@app.route('/Sync/<video_id>')
def sync_video(video_id):
    try:
        add_queue(video_id)
    except Exception as e:
        logger.error(e)
    return ''
