"""Create youtube_dl object"""

import youtube_dl
import sys
import os
from app.config import YDLConfig
from app.project_logging import logger
from typing import Dict, Any

APP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_PATH)
sys.path.insert(0, os.getcwd())


class YDLParams(YDLConfig):
    """create parameters for ydl

    Attributes:
        params (dict): a param dict for ydl

    Args:
        output_folder (str, optional): output path
        downloaded False if not
        mode (str): 'test' or 'live'
    """
    def __init__(self, output_folder: str = '', mode: str = ''):

        params: Dict[Any, Any] = {}
        params['logger'] = logger
        params['format'] = self.video_format
        if mode == 'test':
            params['simulate'] = True
        elif mode == 'live':
            params['simulate'] = False
        else:
            raise ValueError('config mode should be test or live')
        if output_folder != '':
            params['outtmpl'] = os.path.join(output_folder, self.outtmpl)

        self.params = params


class YoutubeDl(YDLParams):
    def __init__(self, output_folder: str, mode: str = ''):
        YDLParams.__init__(self, output_folder, mode)
        self.ydl = youtube_dl.YoutubeDL(params=self.params)
