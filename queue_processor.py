#!/usr/bin/env python3

import sqlite3
import youtube_dl
import os
import sys
import time

app_path = os.path.dirname(__file__)
sys.path.insert(0, app_path)

conn = sqlite3.connect(app_path + '/video_db/queue.db', check_same_thread=False)
#import vtt_to_srt

video_dir = os.path.join('/', 'home', 'pi', 'video/')
subtitles = os.path.join('/', 'home', 'pi', 'subtitles/')


def get_video(video_id):
    """
    Given an id, it youtube-dl can process it, it will download
    the video.

    :param video_id: The unique video identifier 
    """
    opts = {'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': os.path.join(video_dir, '%(title)s.[%(id)s].%(ext)s'),
            'writesubtitles': False,
            'allsubtitles': False,
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


def mark_queue(video_id):
    with conn:
        conn.execute('update queue set processed = ? where id = ?', (1, video_id,))

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


def process_queue():
    while True:
        with conn:
            unprocessed = conn.execute('select id from queue where processed = 0')
            unprocessed = unprocessed.fetchone()
        if unprocessed is not None:
            unprocessed = unprocessed[0]
            get_video(unprocessed)
            mark_queue(unprocessed)
        time.sleep(10)
        #convert_subtitles()

if __name__ == '__main__':
    process_queue()
