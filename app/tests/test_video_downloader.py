#!/usr/bin/env python3
import unittest
from app.queue_processor.video_downloader import video_folder_name
from app.queue_processor.video_downloader import get_path
from app.queue_processor.video_downloader import create_path
from app.queue_processor.video_downloader import get_video
from app.project_logging import logger
import os


from app.sync_video.queue_manager import add_queue, delete_video


class TestVideoFolderName(unittest.TestCase):
    """Test function video_folder_name"""


    def test_01_video_folder_name(self):
        """video_folder_name removes spaces and
        non word characters"""
        x = video_folder_name('!@test   )value')
        self.assertEqual(x, 'test_value')


    def test_02_video_folder_name(self):
        """Invalid value raises type error"""
        with self.assertRaises(TypeError):
            x = video_folder_name(1)



class TestGetPath(unittest.TestCase):
    """Test function get_path"""


    @classmethod
    def setUpClass(cls):
        cls.test_video_id = 'FBgLytbB-uE'
        cls.test_folder = './blurgh/calm_owl'
        delete_video(cls.test_video_id)
        #TODO delete_video should take care of the folders
        if os.path.exists(cls.test_folder):
            os.rmdir(cls.test_folder)
            os.rmdir('./blurgh')

    
    def test_01_get_path(self):
        """raise type error for invalid values
        passed to get_path"""
        with self.assertRaises(TypeError):
            get_path(1,'test')
        with self.assertRaises(TypeError):
            get_path('test', 1)
        with self.assertRaises(TypeError):
            get_path(1,1)


    def test_02_get_path(self):
        """check values for non existant video_id"""
        add_queue(self.test_video_id, 'blurgh')
        x = get_path(self.test_video_id, 'calm owl')
        self.assertEqual(x, {
            'path': self.test_folder, 
            'exists': False})


    def test_03_get_path(self):
        """check values for existing video_id"""
        add_queue(self.test_video_id, 'blurgh')
        os.makedirs(self.test_folder)
        x = get_path(self.test_video_id, 'calm_owl')
        self.assertEqual(x, {
            'path': self.test_folder, 
            'exists': True})


    @classmethod
    def tearDownClass(cls):
        delete_video(cls.test_video_id)


class TestCreatePath(unittest.TestCase):
    """Test function create_path"""

    @classmethod
    def setUpClass(cls):
        cls.test_video_id = 'FBgLytbB-uE'
        delete_video(cls.test_video_id)


    def test_01_create_path(self):
        """path should be video_dir/subdirs/title"""
        add_queue(self.test_video_id, 'blurgh')
        create_path(self.test_video_id, 'calm owl')
        self.assertTrue(os.path.exists('./blurgh/calm_owl'))


    @classmethod
    def tearDownClass(cls):
        pass
        delete_video(cls.test_video_id)
        #os.rmdir('./blurgh/calm_owl')
        #os.rmdir('./blurgh')


class TestGetVideo(unittest.TestCase):
    """Test function get_video"""


    def test_01_get_video(self):
        """download non existant video"""
        add_queue('FBgLytbB-uE', 'blurgh')
        get_video('FBgLytbB-uE', 'calm owl', 'test')
        delete_video('FBgLytbB-uE')


if __name__ == '__main__':
    unittest.main()
