#!/usr/bin/env python3

import os
import sys
import pymongo
from string import Template

BASE_PATH = '/mnt/files/share/'

CLIENT = pymongo.MongoClient()
DATABASE = CLIENT['video']
COLLECTION = DATABASE['videos']

tagged = [(i['tags']) for i in COLLECTION.find() if 'tags' in i.keys()]

flat = []

for i in tagged:
    if type(i) == list:
        for j in i:
            flat.append(j)
    else:
        flat.append(i)

folders = tuple(set(flat))

def create_path(folder):
    if not os.path.exists(BASE_PATH + folder):
        os.mkdir(BASE_PATH + folder)

for i in folders:
    create_path(i)

"""
[name]
wide links = yes
follow symlinks = yes
comment = name
browseable = yes
path = BASE_PATH + name
guest ok = yes
read only = yes
create mask = 0700
"""

samba_template = Template('[$name]\n \
    wide links = yes\n \
    follow symlinks = yes\n \
    comment = $name\n \
    browseable = yes\n \
    path = $path$name\n \
    guest ok = yes\n \
    read only = yes\n \
    create mask = 0700')

if __name__ == '__main__':
    t = samba_template.substitute(name=sys.argv[1], path=BASE_PATH)
    print(t)
