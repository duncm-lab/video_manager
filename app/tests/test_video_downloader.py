#!/usr/bin/env python3
import unittest
import os

from app.queue_processor.video_downloader import FolderManager, VideoDownloader
from app.queue_processor.video import Video
from app.project_logging import logger
from app.sync_video.queue_manager import add_queue, delete_video


test_video_id = 'FBgLytbB-uE'
test_video_name = 'calm owl'
test_tag0 = 'blurgh'
test_dir0 = test_tag0
test_tag1 = ['blurgh', 'yarr']
test_dir1 = 'blurgh/yarr'
test_path = os.path.join('.', test_dir, 'calm_owl')


class TestFolderManager(unittest.TestCase):


    def setUp():
        """Setup the environment before testing"""

        delete_video(test_video_id)

        if os.path.exists(test_path):
            paths = [i[0], for i in os.walk(test_path)]
            while paths != []:
                path = paths.pop(0)
                os.rmdir(path)


    def test_01_video_folder_name(self):
        """method sanitizes input"""

        vid = Video('!( test video _+_' , 'n/a')
        x = FolderManager(vid)
        self.assertEqual(x.video_folder_name(), 'test_video')


    def test_02_get_path(self):
        """method returns True for key 'exists' when 
        path exists"""

        os.makedirs(test_path)
        add_queue(test_video_id, test_dir)
        vid = Video(test_video_name, test_video_id)
        fm = FolderManager(vid)
        gp = fm.get_path()
        self.assertEqual(gp['path'], test_dir0)
        self.assertEqual(gp['exists'], True)


    def test_03_get_path(self):
        """method returns False for key 'exists' when
        path does not exist"""

        vid = Video(test_video_name, test_video_id)
        fm = FolderManager(vid)
        gp = fm.get_path()
        self.assertEqual(gp['path'], test_path)
        self.assertEqual(gp['exists'], False)


    def test_04_get_path(self):
        """Test when no document exists in db"""
        vid = Video(test_video_name, test_video_id)
        fm = FolderManager(vid)
        gp = fm.get_path()


class TestVideoDownloader(unittest.TestCase):
    pass



if __name__ == '__main__':
    unittest.main()
