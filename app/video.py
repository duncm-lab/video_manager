#!/usr/bin/env python3
"""Interact with video documents and objects
"""
import os
from typing import Union, List, Optional, Tuple
import shutil
from app.database import COLLECTION
from app.project_logging import logger


class Video:

    """CRUD operations for video documents

    Args:
        mode (str): when in test mode, alterations to data is prevented
        video_id (str): video id
        processed (bool): flag for if the video has been downloaded
        title (str): video title
        uploader (str): channel name
        upload_date (str): date of video upload
        description (str): description of video
        thumbnail (str): url of thumbnail image
        tags (list): A single string or list of strings
        file_path (str): files location
    """

    def __init__(self,
                 mode: str,
                 video_id: str,
                 processed: bool,
                 title: str,
                 uploader: str,
                 upload_date: str,
                 description: str,
                 thumbnail: str,
                 tags: List[str],
                 file_path: str):

        logger.info('Video object initialised')

        self._mode = mode
        self._video_id: str = video_id
        self._processed: bool = processed
        self._title: str = title
        self._uploader: str = uploader
        self._upload_date: str = upload_date
        self._description: str = description
        self._thumbnail: str = thumbnail
        self._tags: Optional[List[str]] = tags
        self._file_path: str = file_path
        self._processing: bool = False

    def __repr__(self) -> str:
        """Object repr
        Return:
            str: repr
        """
        return 'Video(' \
               f'\'{self._mode}\', ' \
               f'\'{self._video_id}\', ' \
               f'{self._processed}, ' \
               f'\'{self._title}\', ' \
               f'\'{self._uploader}\', ' \
               f'\'{self._upload_date}\', ' \
               f'\'{self._description}\', ' \
               f'\'{self._thumbnail}\', ' \
               f'\'{self._tags}\', ' \
               f'\'{self._file_path}\')'

    @property
    def mode(self) -> str:
        """test or live mode

        Return:
            str: mode
        """
        return self._mode

    @property
    def video_id(self) -> str:
        """unique id of video
        Return:
            str: video id
        """
        return self._video_id

    @property
    def processed(self) -> bool:
        """flag for whether the video has been downloaded
        Return:
            bool: processed
        Raises:
            ValueError: attempt to set as non bool
        """
        return self._processed

    @processed.setter
    def processed(self, p: bool) -> None:
        if not isinstance(p, bool):
            raise ValueError('processed must be bool')
        self._processed = p
        logger.info('processed attribute set to %s', str(p))

    @property
    def title(self) -> str:
        """title of video
        Return:
            str: title
        """
        return self._title

    @property
    def uploader(self) -> str:
        """User who uploaded video
        Return:
            str: uploader
        """
        return self._uploader

    @property
    def upload_date(self) -> str:
        """date video uploaded
        Return:
            str: upload date
        """
        return self._upload_date

    @property
    def description(self) -> str:
        """description of video
        Return:
            str: description
        """
        return self._description

    @property
    def thumbnail(self) -> str:
        """Thumbnail url
        Return:
            str: thumbnail url
        """
        return self._thumbnail

    @property
    def tags(self) -> Optional[List[str]]:
        """Tags
        Return:
            list: list of tags
        """
        if self._tags in [None, '', []]:
            return ['undefined']
        else:
            return self._tags

    @property
    def file_path(self) -> str:
        """file path location on disk
        Return:
            str: file path
        Raises:
            ValueError: attempt to set as non bool
        """
        return self._file_path

    @file_path.setter
    def file_path(self, path: str) -> None:
        if not isinstance(path, str):
            raise ValueError('Path must be str')
        self._file_path = path
        logger.info('file_path attribute set to %s', path)

    @property
    def processing(self) -> bool:
        """Check if Video is currently
        being processed

        Return:
            bool: processing status
        Raises:
            ValueError: attempt to set as non bool
        """
        return self._processing

    @processing.setter
    def processing(self, p: bool) -> None:
        if not isinstance(p, bool):
            raise ValueError('processing flag must be bool')
        self._processing = p
        logger.info('processing attribute set to %s', str(p))

    def delete_video(self, check: bool = False) -> Union[Tuple, str]:
        """Remove the current object from the database
        along with any files or folders

        Args:
            check (bool): a value to be explicitly set
            in order for the video to be deleted

        Returns:
           tuple: (int: 0, str: '') - the document was not found
           tuple: (int: 1, str: '') - the document was found and deleted
            but had not path key
           tuple: (int: 2, str: '') - the document and path were found
            both were deleted
           str: check did not pass
        """

        if self._mode == 'test':
            return 'Data cannot be deleted in test mode'

        if not check:
            return ''

        result = COLLECTION.find_one({'_id': self.video_id},
                                     {'_id': True, 'path': True})

        if not result:
            res = (0, '')
        elif 'path' not in result.keys():
            COLLECTION.delete_one({'_id': self.video_id})
            res = (1, '')
            logger.info('video_id %s deleted - no folder found', self.video_id)
        else:
            COLLECTION.delete_one({'_id': self.video_id})
            path: str = result['path']
            try:
                shutil.rmtree(os.path.split(path)[0], ignore_errors=True)
            except FileNotFoundError as e:
                logger.error(e)
            res = (2, path)
            logger.info('video_id %s deleted - folder %s deleted',
                        self.video_id, path)

        return res

    def save_video(self) -> Union[None, str]:
        """save the Video instance to the database

        Return:
            None: success
            str: test mode message
        """

        if self._mode == 'test':
            return 'Data cannot be saved in test mode'

        dct = self.__dict__
        doc = {}

        # pop the private modifier of the attribute name before saving
        for k, v in dct.items():
            if k == '_video_id':
                doc['_id'] = v
            elif k == '_processed':
                doc['Processed'] = v
            else:
                dk = k.lstrip('_')
                doc[dk] = v

        COLLECTION.replace_one({'_id': self._video_id}, doc)
        logger.info('%s updated', self._video_id)
        return None


class VideoSearch:
    """find videos"""

    @staticmethod
    def query_result_to_video(result: dict,
                              mode: str = '') -> Union[None, Video]:
        """Take a video document and convert it to
        a Video instance

        Args:
            result (dict): A document from the database
            mode (str): Set the mode for the video object

        Returns:
            Video: an instance of the Video class
        """

        vid = result['_id']
        processed = result['Processed']
        title = result['title']
        uploader = result['uploader']
        upload_date = result['upload_date']
        description = result['description']
        thumbnail = result['thumbnail']
        if 'tags' in result.keys():
            tags = result['tags']
        else:
            tags = 'undefined'
        if 'file_path' in result.keys():
            file_path = result['file_path']
        else:
            file_path = ''

        ret = Video(mode, vid, processed, title, uploader, upload_date,
                    description, thumbnail, tags, file_path)

        return ret

    @staticmethod
    def get_next_unprocessed(mode: str = '') -> Union[None, Video]:
        """Find the next unprocessed video

        Args:
            mode (str): mode flag to pass to Video

        Returns:
            Video: A Video instance
            None: no value found
        """
        res = COLLECTION.find_one({'Processed': False})

        if res:
            ret = VideoSearch.query_result_to_video(res, mode)
        else:
            ret = None

        return ret

    @staticmethod
    def exact_find_video(**kwarg: str) -> Union[Video, None]:
        """ match a value exactly

        Args:
            kwarg (dict): kv corresponding to value in db

        Return:
            Video: an instance of Video
            None: no value found

        """

        search = COLLECTION.find_one(kwarg)
        if search:
            ret = VideoSearch.query_result_to_video(search)
        else:
            ret = None

        return ret
