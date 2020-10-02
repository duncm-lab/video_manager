#!/usr/bin/env python3
import sys
import requests

url = 'http://localhost:8080/Sync/'

video_id = sys.argv[1]
tags = sys.argv[2]

requests.get(url + video_id + '/' + tags)
