#!/usr/bin/env python3
# pylint: disable=all
import requests
import sys

for i in sys.argv[1:]:
    try:
        r = requests.get(f'http://localhost:8080/delete/{i}')
        print(r.text)
    except:
        continue

