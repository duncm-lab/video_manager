#!/usr/bin/env python3
"""Downloads data and creates related folders
"""

import os
import sys
import youtube_dl
import re


APP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_PATH)
sys.path.insert(0, os.getcwd())

from app.config import VIDEO_DIR # pylint: disable=wrong-import-position
from app.config import PROCESS_YOUTUBE_DL_PARAMS # pylint: disable=wrong-import-position
from app.database import COLLECTION # pylint: disable=wrong-import-position
from app.project_logging import logger # pylint: disable=wrong-import-position



def video_folder_name(title: str) -> str:
    """ Sanitize the folder name of invalid posixpath characters

    Args:
        title (str): name to be sanitized

    Returns:
        (str) sanitized folder name

    """
    re_comp0 = re.compile('[^A-Za-z0-9.]')
    re_comp1 = re.compile('_{2,}')
    return re_comp1.sub('_', re_comp0.sub('_', title))


def get_path(video_id: str, title: str) -> dict:
    """Return folder path for video if it exists

    Args:
        video_id (str): youtube video id
        title (str): video title

    Returns:
        dict: {path: True || False} if path does or doesn't exist

    Raises:
        TypeError: supplied tags not type str or list
    """
    tags: str = COLLECTION.find_one({'_id': video_id}, {'tags': True})['tags']

    if isinstance(tags, list): # TODO check list of strings
        sub_dir = '/'.join(tags)
    elif isinstance(tags, str):
        sub_dir = tags
    else:
        raise TypeError(f'Invalid tag type {type(tags)}')

    path: str = os.path.join(VIDEO_DIR, sub_dir, video_folder_name(title))
    if os.path.exists(path):
        result = {'path': path, 'exists': True}
    else:
        result = {'path': path, 'exists': False}

    return result


def create_path(video_id: str, title: str) -> None:
    """Create folder for video from tags

    Args:
        video_id (str): youtube video id
        title (str): video title
    """
    check = get_path(video_id, title)
    exists: bool = check.__getitem__('exists')
    path: str = check.__getitem__('path')

    if not exists:
        logger.info('Creating path %s', path)
        os.makedirs(path)
    else:
        logger.info('Existing path %s found', path)



def get_video(video_id: str, title: str) -> None:
    """ Download video

    Args:
        video_id (str): id of youtube video
        title (str): title of video
    """

    create_path(video_id, title)
    output_folder = get_path(video_id, title)['path']
    opts = PROCESS_YOUTUBE_DL_PARAMS
    opts['outtmpl'] = os.path.join(output_folder, '%(title)s.%(ext)s')
    opts['logger'] = logger

    try:
        with youtube_dl.YoutubeDL(opts) as ydl:
            info_dict = ydl.extract_info(video_id)
            ydl.process_info(info_dict)
    except (youtube_dl.utils.DownloadError, \
            youtube_dl.utils.SameFileError) as e:
        logger.error(e)
        logger.info('failed to download video %s,'
                'calling failback function generic_video', video_id)
        pass

