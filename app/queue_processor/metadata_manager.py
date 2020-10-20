#!/home/dunc/systools/python/bin/python3.8
"""Create meta data files for video"""

import os
import sys
import requests
import io
from PIL import Image
from string import Template

APP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_PATH)
sys.path.insert(0, os.getcwd())

from app.project_logging import logger # pylint: disable=wrong-import-position
from app.database import COLLECTION # pylint: disable=wrong-import-position
from app.queue_processor.video_downloader import get_path # pylint: disable=wrong-import-position


def get_thumbnail(video_id: str, title: str) -> None:
    #TODO fix path to use same as video_downloader
    """Download thumbnail to path

    Args:
        video_id (str): id of video
        title (str): title of video
    """
    url = COLLECTION.find_one({'_id': video_id}, \
            {'thumbnail': True})['thumbnail']
    data = requests.get(url, stream=True)
    image_data = Image.open(io.BytesIO(data.content))
    path = get_path(video_id, title)['path']
    logger.info('writing thumbnail to path %s', path)
    image_data.save(os.path.join(path, 'thumbnail.jpg'), 'jpeg')


def write_nfo(video_id: str, title: str) -> None:
    """ Create an nfo file and write to path
    Args:
        video_id (str): id of video
        title (str): title of video
    """
    path = get_path(video_id, title)['path']
    i = COLLECTION.find_one({'_id': video_id}, {'_id': True,
        'uploader': True, 'title': True,
        'description': True, 'upload_date': True})

    try:
        with open(os.path.join(APP_PATH, 'template.nfo'), 'r') as fl:
            template = Template(fl.read())
    except FileNotFoundError as e:
        logger.error(e)

    out_template = template.substitute(
            unique_id=i['_id'], \
            studio=i['uploader'], \
            title=i['title'], \
            plot=i['description'], \
            date_prem=i['upload_date'])
    path = os.path.join(get_path(video_id, title)['path'], 'tvshow.nfo')
    logger.info('writing nfo to path %s', path)
    with open(path, 'w') as fl:
        fl.write(out_template)
