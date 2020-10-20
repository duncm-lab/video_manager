#!/usr/bin/env python3
"""Download and process videos with youtube_dl
"""

import os
import sys
import time

APP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_PATH)
sys.path.insert(0, os.getcwd())

from app.project_logging import logger # pylint: disable=wrong-import-position
from app.database import COLLECTION # pylint: disable=wrong-import-position
from app.queue_processor.video_downloader import get_video # pylint: disable=wrong-import-position
from app.queue_processor.metadata_manager import write_nfo, get_thumbnail # pylint: disable=wrong-import-position


def mark_queue(video_id: str) -> None:
    """Update database to mark item as processed

    Args:
        video_id (str): id of video
    """
    logger.info('Setting %s as processed', video_id)
    COLLECTION.update_one({'_id': video_id}, {'$set': {'Processed': True}})


def process_queue() -> None:
    """Loop and check for new records and call
    processing functions if found"""
    while True:
        unprocessed = COLLECTION.find({'Processed': False}, {'_id': True, \
            'title': True, 'thumbnail': True})
        for i in unprocessed:
            get_video(i['_id'], i['title'])
            mark_queue(i['_id'])
            write_nfo(i['_id'], i['title'])
            get_thumbnail(i['_id'], i['title'])


        time.sleep(10)


if __name__ == '__main__':
    process_queue()
