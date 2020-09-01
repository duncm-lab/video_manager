#!/usr/bin/env python3

#import sqlite3
import youtube_dl
import os
import sys
import time
import pymongo
from string import Template
import requests
from PIL import Image
import io
import subprocess

client = pymongo.MongoClient()
database = client['video']
collection = database['videos']
kodi = 'root@192.168.1.232' # ssh keys shared


app_path = os.path.dirname(__file__)
sys.path.insert(0, app_path)

#conn = sqlite3.connect(app_path + '/video_db/queue.db', check_same_thread=False)
#import vtt_to_srt

video_dir = os.path.join('/', 'home', 'ubuntu', 'video/')
subtitles = os.path.join('/', 'home', 'ubuntu', 'subtitles/')

def add_paths_to_db(video_id, path, filename):
    collection.update_one({'_id': video_id}, {'$set': {'path': path}})
    collection.update_one({'_id': video_id}, 
            {'$set': {'filename': os.path.join(path, filename)}})

def video_folder_name(title):
    return title.replace(' ', '_').replace("'", "")

def get_video(video_id, title):
    """
    Given an id, youtube-dl can will download
    the video.

    :param video_id: The unique video identifier 
    """
    path = os.path.join(video_dir, video_folder_name(title))
    if os.path.exists(path) is False:
        os.mkdir(path)

    opts = {'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': os.path.join(video_dir, video_folder_name(title), '%(title)s.%(ext)s'),
            'writesubtitles': False,
            'allsubtitles': False,
            'writethumbnail': False,
            'writedescription': False,
            'subtititleslang': 'en'}

    try:
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([video_id])
    except youtube_dl.utils.DownloadError:
        generic_video(video_id)




def generic_video(link):
    opts = {'outtmpl': video_dir + '%(title)s.%(ext)s',
            'default_search': 'auto'}
            
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([link])

def write_nfo(video_id, title):
    i = collection.find_one({'_id': video_id})
    with open('template.nfo', 'r') as fl:
        template = Template(fl.read())
    out_template = template.substitute(unique_id=i['_id'], studio=i['uploader'],
            title=i['title'], plot=i['description'])
    path = os.path.join(video_dir, video_folder_name(title), 'tvshow.nfo')
    with open(path, 'w') as fl:
        fl.write(out_template)





def mark_queue(video_id):
    #with conn:
    #    conn.execute('update queue set processed = ? where id = ?', (1, video_id,))
    collection.update_one({'_id': video_id}, {'$set': {'Processed': True}})

#def convert_subtitles():
#    """
#    convert vtt to srt for kodi
#    """
#    vtt_files = [i for i in os.listdir(video_dir) if i.endswith('vtt')]
#
#    for i in vtt_files:
#        try:
#            vtt_file = os.path.join(video_dir, i)
#            vtt_to_srt(vtt_file)
#            srt_file = vtt_file.replace('.vtt', '.srt')
#            subtitle_path = os.path.join(subtitles, os.path.split(srt_file)[1])
#            os.rename(srt_file, subtitle_path)
#            os.remove(vtt_file)
#            
#        except FileNotFoundError:
#            print('No Subtitles for {}'.format(i))

def get_thumbnail(url, title):
    data = requests.get(url, stream=True)
    image_data = Image.open(io.BytesIO(data.content))
    path = os.path.join(video_dir, video_folder_name(title), 'thumbnail.jpg') 
    image_data.save(path, 'jpeg')


def process_queue():
    while True:
        #unprocessed = conn.execute('select id from queue where processed = 0')
        unprocessed = [i for i in collection.find({'Processed': False}, {'_id': True, 
            'title': True, 'thumbnail': True})]
        for i in unprocessed:
            get_video(i['_id'], i['title'])
            mark_queue(i['_id'])
            write_nfo(i['_id'], i['title'])
            get_thumbnail(i['thumbnail'], i['title'])

        time.sleep(10)


if __name__ == '__main__':
    process_queue()
