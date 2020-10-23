#!/usr/bin/env python3
import unittest


from app.config import YDLConfig, LogConfig, DBConfig
from app.config import load_config


class TestDBConfig(unittest.TestCase):

    def test_config_attrs(self):
        """Assert all attributes match those in config file"""
        x = load_config('mongo_db')
        self.assertEqual(DBConfig.mongo_server, x['mongo_server'])
        self.assertEqual(DBConfig.mongo_collection, x['mongo_collection'])
        self.assertEqual(DBConfig.mongo_database, x['mongo_database'])


class TestYDLConfig(unittest.TestCase):

    def test_config_attrs(self):
        """Assert all attributes match those in config file"""
        x = load_config('youtube_dl')
        self.assertEqual(YDLConfig.video_format, x['video_format'])
        self.assertEqual(YDLConfig.outtmpl, x['outtmpl'])
        self.assertEqual(YDLConfig.video_dir, x['video_dir'])


class TestLogConfig(unittest.TestCase):

    def test_config_attrs(self):
        """Assert all attributes match those in config file"""
        x = load_config('logging')
        self.assertEqual(LogConfig.log_level, x['log_level'])
        self.assertEqual(LogConfig.log_location, x['log_location'])


if __name__ == '__main__':
    unittest.main()
