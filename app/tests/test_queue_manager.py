#!/usr/bin/env python3
import unittest

from app.sync_video.queue_manager import get_video_info, check_db, add_queue
from app.sync_video.queue_manager import delete_video
from app.project_logging import logger


class TestGetVideoInfo(unittest.TestCase):


    def test_01_get_video_info(self):
        """ Assert invalid value exception logged
        and None returned"""

        with self.assertLogs(logger=logger, level='ERROR'):
            res = get_video_info('invalid')
        self.assertEqual(res, None)

    def test_02_get_video_info(self):
        """Assert a dictionary is returned when a valid
        video_id is passed"""
        res = get_video_info('FBgLytbB-uE')
        self.assertEqual(type(res), dict)

    def test_03_get_video_info(self):
        """Assert TypeError exeception raised when invalid data
        type passed to function and None returned"""

        with self.assertRaises(TypeError):
            get_video_info(1)


class TestCheckDB(unittest.TestCase):


    def test_01_check_db(self):
        """non existant value in db returns False"""
        res = check_db('non_existant')
        self.assertEqual(res, False)


    def test_02_check_db(self):
        """Assert error logger video_id of wrong
        data type and returns None"""

        with self.assertRaises(TypeError):
            ret = check_db(1)
            self.assertEqual(type(ret), None)

class TestAddQueue(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.test_video_id = 'FBgLytbB-uE'
        delete_video(cls.test_video_id)


    def test_01_add_queue(self):
        """TypeError raised for invalid video_id type
        and None is returned"""

        with self.assertRaises(TypeError):
            ret = add_queue(1)
            self.assertEqual(type(ret), None)


    def test_02_add_queue(self):
        """Assert video can be added to database
        and info message logged"""
        with self.assertLogs(logger=logger, level='INFO'):
            res = add_queue(self.test_video_id)
            self.assertEqual(res, True)


    def test_03_add_queue(self):
        """Assert duplicate video id logs an info
        message and returns false"""
        with self.assertLogs(logger=logger, level='INFO'):
            add_queue(self.test_video_id)
            res = add_queue(self.test_video_id)

            self.assertEqual(res, False)


    @classmethod
    def tearDownClass(cls):
        delete_video(cls.test_video_id)


if __name__ == '__main__':
    unittest.main()

