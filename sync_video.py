#!/usr/bin/env python3
from __future__ import unicode_literals
import web
from video_db import list_videos, check_exists, delete_removed
import youtube_dl

def get_video(video_id):
    opts = {'download_archive': 'archive',
            'format': 'bestvideo+bestaudio',
            'outtmpl': '~/external/video/%(title)s.[%(id)s].%(ext)s'}
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([video_id])



urls = ('/', 'Index',
        '/save', 'SaveVideo',
        '/sync', 'SyncVideo'
        )

class Index:
    def GET(self):
        return 'Index'

class SaveVideo:
    def GET(self):
        video_id = web.input(id=0)
        if check_exists(video_id.id) == False:
            insert_video(video_id.id)

class SyncVideo:
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
