#!/usr/bin/env python3
import os
import pymongo
import re


RE_FILE_EXTENSION = re.compile('\.\w+$')

BASE_PATH = '/mnt/files/share/'

CLIENT = pymongo.MongoClient()
DATABASE = CLIENT['video']
COLLECTION = DATABASE['videos']

def database_lookup():
    database_lookup = COLLECTION.find({}, {'_id': True, 'title': True, 'tags': True})
    return [i for i in database_lookup]

tagged_items = [i for i in database_lookup()
        if 'tags' in i.keys()
        and i['tags'] != []]

tagged_names = [i['title'] for i in tagged_items]

video_folders = [i.path for i in os.scandir(BASE_PATH + 'video')]

staging = []

"""
Use the filename to determine the database entry,
this is due to the folder names being sanitized
of bad path characters
"""
for i in video_folders:
    files = os.listdir(i)
    if len(files) != 3:
        print(i)
    filename = [f for f in files if f not in ['thumbnail.jpg', 'tvshow.nfo']][0]
    title = filename.replace(RE_FILE_EXTENSION.search(filename).group(), '')
    if title in tagged_names:
        index = tagged_names.index(title)
        item = tagged_items[index]
        item['filename'] = filename
        item['folder'] = i
        staging.append(item)

for i in staging:
    for j in i['tags']:
        #os.symlink(i['folder'], BASE_PATH + j + '/' + title)
        src = i['folder']
        dst = BASE_PATH + j + '/' + i['title']
        if not os.path.exists(dst):
            os.symlink(src, dst)
        
