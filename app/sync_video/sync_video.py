#!/usr/bin/env python3
from __future__ import unicode_literals
import sys
import os
import web

APP_PATH = os.path.dirname(__file__)
sys.path.insert(0, APP_PATH)

from add_to_queue import add_queue


URLS = ('/', 'Index',
        '/syncWL', 'SyncWatchLater',
        '/Sync', 'SyncVideo'
        )


class SyncVideo:
    def GET(self):
        try:
            video_id = web.input(video_id=0)
            add_queue(video_id.video_id)
        except Exception as e:
            with open('sync_exception.log', 'w') as fl:
                fl.write(str(e))


class Index:
    def GET(self):
        
        return '<h1>Index</h1>'


class SyncWatchLater:
    """Check the watch later list and removed
    any videos not listed there"""
    def GET(self):
        video_ids = web.input(video_ids=0)
        wl_videos = video_ids.video_ids.split(',')
        for video in wl_videos:
            get_video(video)


#application = web.application(URLS, globals()).wsgifunc()
try:
    application = web.application(URLS, globals())
except Exception as e:
    with open('app.log', 'w') as fl:
        fl.write(str(e))

if __name__ == '__main__':
    application.run()
