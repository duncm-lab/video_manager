#!/usr/bin/env python3
"""Add unprocessed items to the database
"""

import youtube_dl
from datetime import datetime
from typing import Union, List


from app.database import COLLECTION
from app.project_logging import logger
from app.ydl import YoutubeDl


ydl = YoutubeDl(output_folder='', mode='test')
INFO_EXTRACTOR = ydl.ydl


def get_video_info(video_id: str,
                   tags: List = None) -> Union[None, dict]:
    """get metadata for video

    Args:
        video_id (str): The id of a youtube video
        tags (list): A list of tags

    Returns:
        None: if exception
        dict: example

        {'_id': 'video_id',
        'Processed': False,
        'title': 'video title',
        'uploader': 'video creator',
        'upload_date': 'video upload date (%Y%m%d)'
        'description': 'video description',
        'thumbnail': 'video thumbnail (url)',
        'tags': [tags]}

    Raises:
        TypeError: invalid video_id type

    """

    if not isinstance(video_id, str):
        raise TypeError(f'{video_id} should be str not {type(video_id)}')
    if tags is None:
        tags = []

    try:
        video_info = INFO_EXTRACTOR.extract_info(video_id)
    except youtube_dl.utils.DownloadError as e:
        logger.error(e)
        logger.info('%s is not a valid id', video_id)
        return None

    info = {
        '_id': video_info['id'],
        'Processed': False,
        'title': video_info['title'],
        'uploader': video_info['uploader'],
        'upload_date': datetime.strptime(video_info['upload_date'], '%Y%m%d'),
        'description': video_info['description'],
        'thumbnail': video_info['thumbnail'],
        'tags': tags}

    return info


def check_db(video_id: str) -> bool:
    """Query the database and assert if the value exists.

    Args:
        video_id (str): The id of a youtube video

    Returns:
        False: if video does not exist
        True: if video does exist

    Raises:
        TypeError: invalid video_id type
    """

    if not isinstance(video_id, str):
        raise TypeError(f'{video_id} should be str not {type(video_id)}')

    result = [i['_id'] for i in COLLECTION.find({'_id': video_id})]

    if not result:
        ret = False
    else:
        ret = True
    return ret


def add_queue(video_id: str, tags: list = None) -> bool:
    """If the video_id does not exist, insert
    an entry into the database from the information
    provided by get_video_info

    Args:
        video_id (str): The id of a youtube video
        tags (list): A list of tags

    Returns:
        True: item was added
        False: exception occurred

    Raises:
        TypeError: invalid video_id type
    """
    ret = False
    vid_info = None

    if tags is None:
        tags = ['undefined']
    if not isinstance(video_id, str):
        raise TypeError(f'{video_id} should be str not {type(video_id)}')

    if check_db(video_id) is True:
        logger.info('video_id %s already exists in database', video_id)
        ret = False
    else:
        vid_info = get_video_info(video_id, tags)

    if vid_info is not None:
        COLLECTION.insert_one(get_video_info(video_id, tags))
        logger.info('%s successfully inserted', video_id)
        ret = True

    return ret
