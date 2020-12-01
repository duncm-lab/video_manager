#!/usr/bin/env python3
"""Config parameters for application

This file is to be copied into each docker image. It is also
used by auxiliary tools.
"""
# see help(youtube_dl.YoutubeDL) for list of params
from config_loader import load_config
from typing import Any, Dict


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
