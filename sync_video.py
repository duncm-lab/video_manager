#!/usr/bin/env python3
from __future__ import unicode_literals
import web
from queue_processor import add_queue




urls = ('/', 'Index',
        '/syncWL', 'SyncWatchLater',
        '/Sync', 'SyncVideo'
        )


class SyncVideo:
    def GET(self):
        video_id = web.input(video_id=0)
        add_queue(video_id.video_id)


class Index:
    def GET(self):
        return 'Index'


class SyncWatchLater:
    """Check the watch later list and removed
    any videos not listed there"""
    def GET(self):
        video_ids = web.input(video_ids=0)
        wl_videos = video_ids.video_ids.split(',')
        for video in wl_videos:
            get_video(video)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
