#!/usr/bin/env python3
"""Create meta data files for video"""

import os
import requests
import io
from PIL import Image
from string import Template

from app.project_logging import logger
from app.database import COLLECTION
from app.queue_processor.video_downloader import FolderManager
from app.video import Video

APP_PATH = os.path.dirname(os.path.abspath(__file__))


class MetadataManager(FolderManager):
    """Handle metadata such as thumbnail.jpg and
    nfo file

    Args:
        video_id (str): id of video
        title (str): video title

    Attributes:
        video_id (str): id of video
        title (str): video title"""

    def __init__(self, vid: Video):
        super().__init__(vid)
        self.video_id: str = vid.video_id
        self.title: str = vid.title

    def get_thumbnail(self) -> None:
        # TODO fix path to use same as video_downloader
        """Download thumbnail to path
        """
        url = COLLECTION.find_one({'_id': self.video_id},
                                  {'thumbnail': True})['thumbnail']
        data = requests.get(url, stream=True)
        image_data = Image.open(io.BytesIO(data.content))
        path = self.get_path()['path']
        logger.info('writing thumbnail to path %s', path)
        image_data.save(os.path.join(path, 'thumbnail.jpg'), 'jpeg')
    
    def write_nfo(self) -> None:
        """ Create an nfo file and write to path"""

        i = COLLECTION.find_one({'_id': self.video_id},
                                {'_id': True, 'uploader': True, 'title': True,
                                 'description': True, 'upload_date': True})
    
        try:
            with open(os.path.join(APP_PATH, 'template.nfo'), 'r') as fl:
                template = Template(fl.read())
        except FileNotFoundError as e:
            logger.error(e)
    
        out_template = template.substitute(
                unique_id=i['_id'],
                studio=i['uploader'],
                title=i['title'],
                plot=i['description'],
                date_prem=i['upload_date'])
        path = os.path.join(self.get_path()['path'], 'tvshow.nfo')
        logger.info('writing nfo to path %s', path)
        with open(path, 'w') as fl:
            fl.write(out_template)
