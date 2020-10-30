#!/usr/bin/env python3
"""Download and process videos with youtube_dl
"""

import time
import sys
from app.video import VideoSearch
from app.queue_processor.video_downloader import VideoDownloader
from app.queue_processor.metadata_manager import MetadataManager


def process_queue(mode: str = 'test') -> None:
    """Loop and check for new records and call
    processing functions if found
    """
    while True:
        vid = VideoSearch.get_next_unprocessed()
        if vid:
            vid.processing = True
            vdl = VideoDownloader(vid, mode)
            vdl.get_video()
            meta = MetadataManager(vid)
            meta.get_thumbnail()
            meta.write_nfo()

        time.sleep(10)


if __name__ == '__main__':
    set_mode = "live"
    process_queue(set_mode)
