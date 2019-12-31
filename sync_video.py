#!/usr/bin/env python3
from __future__ import unicode_literals
import web
import youtube_dl

def get_video(video_id):
    opts = {'download_archive': 'archive',
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': '~/external/video/video1/%(title)s.[%(id)s].%(ext)s'}
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([video_id])

def generic_video(link):
    opts = {'download_archive': 'archive',
            'outtmpl': '~/external/video/video2/%(title)s.%(ext)s'}
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([link])

urls = ('/', 'Index',
        '/syncWL', 'SyncWatchLater',
        '/syncPN', 'SyncPN',
        '/Sync', 'SyncVideo'
        )

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

class SyncVideo:
    def GET(self):
        video_id = web.input(video_id=0)
        video_id.video_id
        get_video(video_id.video_id)

class SyncPN:
    def GET(self):
        link = web.input(link=0)
        generic_video(link.link)






if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
