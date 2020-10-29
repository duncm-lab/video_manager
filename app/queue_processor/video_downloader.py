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
from app.video import Video

VIDEO_DIR = YDLConfig.video_dir


class FolderManager:
    def __init__(self, vid: Video):

        self.vid = vid        
        self.title: str = vid.title
        self.video_id: str = vid.video_id

    def video_folder_name(self) -> str:
        """ Sanitize the folder name of invalid posixpath characters
    
        Returns:
            (str) sanitized folder name
    
        Raises:
            TypeError: type of title supplied was invalid
        """
    
        re_comp0 = re.compile('[^A-Za-z0-9.]')
        re_comp1 = re.compile('_{2,}')
        res = re_comp1.sub('_', re_comp0.sub('_', self.title))
        return res.strip('_')
    
    def get_path(self) -> dict:
        """ Build a path from the VIDEO_DIR, tags and title

        Returns:
            dict: {path: True || False} if path does or doesn't exist
    
        Raises:
            TypeError: supplied tags not type str or list
        """
    
        tags: list = COLLECTION.find_one({'_id': self.video_id}, 
                                         {'tags': True})['tags']

        sub_dir = '/'.join(tags)
    
        path: str = os.path.join(VIDEO_DIR, sub_dir, 
                                 self.video_folder_name())
        if os.path.exists(path):
            result = {'path': path, 'exists': True}
        else:
            result = {'path': path, 'exists': False}
    
        return result
    
    def create_path(self) -> None:
        """Create folder for video from tags"""
    
        check = self.get_path()
        exists: bool = check.__getitem__('exists')
        path: str = check.__getitem__('path')
    
        if not exists:
            os.makedirs(path)
            logger.info('Creating path %s', path)
        else:
            logger.info('Existing path %s found', path)


class VideoDownloader(FolderManager):
    """Create relevant paths and download video
    Args:
        vid (Video): Instance of Video class

    Attributes:
        title (str): video title
        video_id (str): video id
        
    """
    
    def __init__(self, vid: Video, mode: str):
        if vid.processed:
            raise ValueError(f'{vid.video_id} has been processed')
        super().__init__(vid)
        self.mode: str = mode
        
    def get_video(self) -> None:
        """ Download video and write output to folder """
        self.create_path()
    
        output_folder = self.get_path()['path']
        COLLECTION.update_one({'_id': self.video_id}, {'$set':
                                                       {'path': output_folder}})
        y = YoutubeDl(output_folder=output_folder, mode=self.mode)
        ydl = y.ydl

        """
        Update the processing attribute to True whilst
        the video is being downloaded so that other 
        processes don't attempt to download the video
        whilst it's in progress. Finally update the
        processed Flag to true and processing Flag to
        False
        """
        try:
            with ydl:
                self.vid.processing = True
                info_dict = ydl.extract_info(self.video_id)
                ydl.process_info(info_dict)
                self.vid.processing = False
                self.vid.processed = True
                self.vid.file_path = output_folder
                self.vid.save_video()
        except (DownloadError, SameFileError) as e:
            logger.error(e)
            logger.info('failed to download video %s', self.video_id)
