#!/usr/bin/env python3
import unittest

from app.sync_video.sync_video import app
from app.sync_video.queue_manager import delete_video
from app.project_logging import logger


class TestSyncVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.test_video_id = 'FBgLytbB-uE'
        delete_video(cls.test_video_id)


    def test_01_index(self):
        """Test we can reach the index page at /"""
        req = self.app.get('/')
        self.assertEqual(req.status_code, 200)


    def test_02_invalid_endpoint(self):
        """Test calls to invalid endpoints"""
        req = self.app.get('/does_not_exist')
        self.assertEqual(req.status_code, 404)


    def test_03_invalid_Sync_video_id(self):
        """pass an non valid video_id to /Sync"""
        with self.assertLogs(logger=logger, level='ERROR'):
            req = self.app.get('/Sync/invalid_value')


    def test_04_invalid_Sync_video_id(self):
        """Check exception logged when non valid video_id passed to /Sync"""
        with self.assertLogs(logger=logger, level='ERROR') as cm:
            req = self.app.get('/Sync/invalid_value')


    def test_05_Sync_valid_video_id_notag(self):
        req = self.app.get(f'/Sync/{self.test_video_id}')
        data = req.get_data(as_text=True)
        self.assertEqual(data, f'{self.test_video_id} added')


    def test_06_Sync_video_tags(self):
        """Check tag args work as expected /Sync/video_id/tag0,tag1"""
        delete_video(self.test_video_id)
        req = self.app.get(f'/Sync/{self.test_video_id}/testing,tag')
        data = req.get_data(as_text=True)
        self.assertEqual(data, f'{self.test_video_id}, testing,tag added')


    @classmethod
    def tearDownClass(cls):
        delete_video(cls.test_video_id)


if __name__ == '__main__':
    unittest.main()

