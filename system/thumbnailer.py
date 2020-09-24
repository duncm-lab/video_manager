#!/usr/bin/env python3
import os
import subprocess
from string import Template

kodi_host = 'root@192.168.1.232'
smb_url = 'smb://192.168.1.135/videos/' 
video_dir = '/home/ubuntu/video/'

#get the files from the video dir
files = [i for i in os.listdir(video_dir)
        if i.split('.')[1] != 'nfo']

files.sort()


def remote_query(sql):
    print(sql)
    subprocess.run(['ssh', kodi_host, 'sqlite3', 
        '/storage/.kodi/userdata/Database/Textures13.db',
        "\"{}\"".format(sql)])

remote_query('delete from path;')


with open('add_images_template.sql', 'r') as fl:
    sql_template = Template(fl.read())


def chunk(x):
    count = x
    out = []
    while count != []:
        print(count)
        out.append(x[0:2])
        count = count[2:]
    return out

for i in chunk(files):
    thumb = smb_url + i[0]
    video = smb_url + i[1]
    print(video)
    sql = sql_template.substitute(folderurl=smb_url,
            videourl=video, texture=thumb)
    print(sql)
    remote_query(sql)
    








