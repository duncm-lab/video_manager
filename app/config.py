#!/usr/bin/env python3
"""Config parameters for application

This file is to be copied into each docker image. It is also
used by auxillary tools.
"""
# see help(youtube_dl.YoutubeDL) for list of params
import yaml
import os
from typing import Any, Dict

path = os.path.dirname(os.path.abspath(__file__))

def load_config(config_section: str) -> dict:
    """Read settings from config.yml
    Args:
        config_section (str): config group key

    Returns:
        dict: configuration settings
    """
    with open(os.path.join(path, 'config.yml'), 'r') as fl:
        cfg = yaml.safe_load(fl.read())
    return cfg[config_section]


class YDLConfig:
    """ Config settings for youtube_dl

    Attributes:
        video_format (str): indicate video quality to download
        outtmpl (str): define how the output filename is structured
        video_dir (str, optional): file output location
    """
    _lcfg: Dict[Any, Any] = load_config('youtube_dl')

    video_format: str = _lcfg['video_format']
    outtmpl: str = _lcfg['outtmpl']
    video_dir = _lcfg['video_dir']


class DBConfig:
    """Database related configuration

    Attributes:
        mongo_server (str): server host
        mongo_database (str): mongo database name
        mongo_collection (str): mongo collection name
    """
    _lcfg: Dict[Any, Any] = load_config('mongo_db')

    mongo_server: str = _lcfg['mongo_server']
    mongo_database: str = _lcfg['mongo_database']
    mongo_collection: str = _lcfg['mongo_collection']


class LogConfig:
    """Logging related configuration

    Attributes:
        log_level (str): python logging level
        log_location (str): log file output location
    """
    _lcfg: Dict[Any, Any] = load_config('logging')
    log_level: str = _lcfg['log_level']
    log_location: str = _lcfg['log_location']
