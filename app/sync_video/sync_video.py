#!/usr/bin/env python3
from __future__ import unicode_literals
import sys
import os
import logging
from flask import Flask
from string import Template

APP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_PATH)
sys.path.insert(0, os.getcwd())

import app.config as cfg
from app.config import BASE_PATH
from add_to_queue import add_queue

logging.basicConfig(filename = cfg.SYNC_VIDEO_LOG,
        level = getattr(logging, cfg.LOG_LEVEL))

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

@app.route('/Sync/<video_id>/<tags>')
def sync_video_tags(video_id, tags):
    if tags.find(',') != -1:
        tags = [tag.lower() for tag in tags.split(',')]
    else:
        tags = tags.lower()
    try:
        add_queue(video_id, tags)
    except Exception as e:
        logger.error(e)
    return ''


@app.route('/samba/<share_name>')
def samba_share(share_name):
 
    """
    Return a share entry for a samba share to be inserted in smb.conf
    
    [name]
    wide links = yes
    follow symlinks = yes
    comment = name
    browseable = yes
    path = BASE_PATH + name
    guest ok = yes
    read only = yes
    create mask = 0700

"""

    samba_template = Template('[$name]\n \
    wide links = yes\n \
    follow symlinks = yes\n \
    comment = $name\n \
    browseable = yes\n \
    path = $path$name\n \
    guest ok = yes\n \
    read only = yes\n \
    create mask = 0700')
    return samba_template.substitute(name=share_name, path=BASE_PATH)
