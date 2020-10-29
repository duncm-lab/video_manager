#!/usr/bin/env python3
import unittest
from app.video import Video, VideoSearch
from app.database import COLLECTION


# TODO find a way to setup environment


class TestVideoAttributes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # update query to file objects with different field states
        query = COLLECTION.find_one()
        query['_id'] = 'testing'
        COLLECTION.insert_one(query)
        copy = COLLECTION.find_one({'_id': 'testing'})
        cls.videoObj = VideoSearch.query_result_to_video(copy)

    def test_set_video_id_raises(self):
        """assert that setting video_id class 
        attribute fails"""
        with self.assertRaises(AttributeError):
            self.videoObj.video_id = 'test'

    def test_set_title_raises(self):
        """assert that setting title class
        attribute fails"""
        with self.assertRaises(AttributeError):
            self.videoObj.title = 'test'

    def test_set_uploader_raises(self):
        """assert that setting uploader class
        attribute fails
        """
        with self.assertRaises(AttributeError):
            self.videoObj.uploader = 'test'

    def test_set_upload_date_raises(self):
        """Assert that setting upload_date
        class attribute fails
        """
        with self.assertRaises(AttributeError):
            self.videoObj.upload_date = 'test'

    def test_set_description_raises(self):
        """ assert that setting description
        class attribute fails
        """
        with self.assertRaises(AttributeError):
            self.videoObj.description = 'test'

    def test_set_thumbnail_raises(self):
        """ assert that setting thumbnail
        class attribute fails
        """
        with self.assertRaises(AttributeError):
            self.videoObj.thumbnail = 'test'

    def test_set_processed_raises(self):
        """test setting processed to a non
        boolean value returns an AssertionError
        """
        with self.assertRaises(AssertionError):
            self.videoObj.processed = 'test'

    def name(self):
        """test setting processing to a non
        boolean value returns an AssertionError
        """
        with self.assertRaises(AssertionError):
            self.videoObj.processing = 'test'

    @classmethod
    def tearDownClass(cls):
        COLLECTION.delete_many({'_id': 'testing'})


class TestVideoMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # update query to file objects with different field states
        query = COLLECTION.find_one()
        query['_id'] = 'testing'
        COLLECTION.insert_one(query)
        copy = COLLECTION.find_one({'_id': 'testing'})
        cls.videoObj = VideoSearch.query_result_to_video(copy)

    @classmethod
    def tearDownClass(cls):
        COLLECTION.delete_many({'_id': 'testing'})
    pass
