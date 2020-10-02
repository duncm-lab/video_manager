#!/usr/bin/env python3
"""
Config parameters for application

This file is to be copied into each docker image. It is also
used by auxillary tools.
"""

SYNC_YOUTUBE_DL_PARAMS = {'simulate': True} # see youtube_dl.YoutubeDL for list of params
MONGO_SERVER = 'mongodb://localhost:27017'
MONGO_DATABASE = 'video'
MONGO_COLLECTION = 'videos'
SYNC_VIDEO_LOG = '/sync_video_logs/sync_video.log'
QUEUE_PROCESSOR_LOG = '/queue_processor_logs/queue_processor.log'
LOG_LEVEL = 'DEBUG'
BASE_PATH = '/mnt/files/share/' # where video folders are located trailing '/' required
VIDEO_DIR = '/mnt/files/share/video/' # main video folder with actual files
                                      # (not symlinks)
PROCESS_YOUTUBE_DL_PARAMS = {
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': '', # leave blank, replaced in application
            'writesubtitles': False,
            'allsubtitles': False,
            'writethumbnail': False,
            'writedescription': False,
            'subtititleslang': 'en',
            'logger': ''} # leave blank, replaced in application


