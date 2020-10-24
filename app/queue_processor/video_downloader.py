#!/usr/bin/env python3
"""Downloads data and creates related folders
"""

import os
import re
from youtube_dl.utils import DownloadError, SameFileError

from app.database import COLLECTION
from app.project_logging import logger
from app.ydl import YoutubeDl
from app.config import YDLConfig

VIDEO_DIR = YDLConfig.video_dir


def video_folder_name(title: str) -> str:
    """ Sanitize the folder name of invalid posixpath characters

    Args:
        title (str): name to be sanitized

    Returns:
        (str) sanitized folder name

    Raises:
        TypeError: type of title supplied was invalid
    """

    if not isinstance(title, str):
        raise TypeError(f'title {title} was of type {type(title)}'
                        'not str')

    re_comp0 = re.compile('[^A-Za-z0-9.]')
    re_comp1 = re.compile('_{2,}')
    res = re_comp1.sub('_', re_comp0.sub('_', title))
    return res.lstrip('_')


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
    if not isinstance(video_id, str) or not isinstance(title, str):
        raise TypeError('Invalid type supplied')

    tags: str = COLLECTION.find_one({'_id': video_id}, {'tags': True})['tags']

    if isinstance(tags, list):  # TODO check list of strings
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
        os.makedirs(path)
        logger.info('Creating path %s', path)
    else:
        logger.info('Existing path %s found', path)


def get_video(video_id: str, title: str, mode: str) -> None:
    """ Download video

    Args:
        video_id (str): id of youtube video
        title (str): title of video
        mode (str): 'test' or 'live'
    """

    create_path(video_id, title)
    output_folder = get_path(video_id, title)['path']
    COLLECTION.update_one({'_id': video_id}, {'$set': {'path': output_folder}})
    y = YoutubeDl(output_folder=output_folder, mode=mode)
    ydl = y.ydl

    try:
        with ydl:
            info_dict = ydl.extract_info(video_id)
            ydl.process_info(info_dict)
    except (DownloadError, SameFileError) as e:
        logger.error(e)
        logger.info('failed to download video %s', video_id)
