#!/usr/bin/env python3
"""Config parameters for application

This file is to be copied into each docker image. It is also
used by auxillary tools.
"""
# see youtube_dl.YoutubeDL for list of params
SYNC_YOUTUBE_DL_PARAMS: dict = {'simulate': True}
MONGO_SERVER: str = 'mongodb://localhost:27017'
MONGO_DATABASE: str = 'video'
MONGO_COLLECTION: str = 'videos'
SYNC_VIDEO_LOG:str = '/logs'
QUEUE_PROCESSOR_LOG: str = '/logs'
LOG_LEVEL: str = 'DEBUG'
# where video folders are located trailing '/' required
BASE_PATH: str = '/mnt/files/share/'
VIDEO_DIR: str = '/mnt/files/share/video/'
PROCESS_YOUTUBE_DL_PARAMS: dict = {
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': '', # leave blank, replaced in application
            'writesubtitles': False,
            'allsubtitles': False,
            'writethumbnail': False,
            'writedescription': False,
            'subtititleslang': 'en',
            'logger': ''} # leave blank, replaced in application


