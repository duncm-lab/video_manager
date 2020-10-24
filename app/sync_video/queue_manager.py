#!/usr/bin/env python3
"""Add unprocessed items to the database
"""

import os
import shutil
import youtube_dl
from datetime import datetime
from typing import Union, List, Tuple


from app.database import COLLECTION
from app.project_logging import logger
from app.ydl import YoutubeDl


ydl = YoutubeDl(output_folder='', mode='test')
INFO_EXTRACTOR = ydl.ydl


def get_video_info(video_id: str,
                   tags: Union[List, str] = None) -> Union[None, dict]:
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

    if result == []:
        ret = False
    else:
        ret = True
    return ret


def add_queue(video_id: str, tags: Union[List, str] = None) -> bool:
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

    if not isinstance(video_id, str):
        raise TypeError(f'{video_id} should be str not {type(video_id)}')

    if check_db(video_id) is True:
        logger.info('video_id %s already exists in database', video_id)
        return False
    else:
        vid_info = get_video_info(video_id, tags)

    if vid_info is not None:
        COLLECTION.insert_one(get_video_info(video_id, tags))
        logger.info('%s successfully inserted', video_id)

    return True


def delete_video(video_id: str) -> Tuple[int, str]:
    """Find and delete a video document from the database and file
    system

    Args:
        video_id (str): video_id

    Returns:
        int: 0 - the document was not found
        int: 1 - the document was found and deleted
        but had not path key
        int: 2 - the document and path were found
        both were deleted
    """

    result = COLLECTION.find_one({'_id': video_id},
                                 {'_id': True, 'path': True})

    if not result:
        res = (0, '')
    elif 'path' not in result.keys():
        COLLECTION.delete_one({'_id': video_id})
        res = (1, '')
        logger.info('video_id %s deleted - no folder found', video_id)
    else:
        COLLECTION.delete_one({'_id': video_id})
        path: str = result['path']
        try:
            shutil.rmtree(os.path.split(path)[0], ignore_errors=True)
        except FileNotFoundError as e:
            logger.error(e)
        res = (2, path)
        logger.info('video_id %s deleted - folder %s deleted',
                    video_id, path)

    return res
