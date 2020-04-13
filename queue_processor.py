#!/usr/bin/env python3
import sqlite3
import youtube_dl
import os
conn = sqlite3.connect('queue.db', check_same_thread=False)
from vtt_to_srt.__main__ import vtt_to_srt

video_dir = '/mnt/video/youtube/'
subtitles = video_dir + '/mnt/video/subtitles/'

def get_video(video_id):
    """
    Given an id, it youtube-dl can process it, it will download
    the video.

    :param video_id: The unique video identifier 
    """
    opts = {'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': video_dir + '/%(title)s.[%(id)s].%(ext)s',
            'writesubtitles': True,
            'allsubtitles': False,
            'subtititleslang': 'en'}

    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([video_id])

def check_db(video_id):
    with conn:
        v = conn.execute("select id from queue where id = ?", (video_id,))

    result = v.fetchone()

    if result == None:
        return False
    else:
        return True


def add_queue(video_id):
    if check_db(video_id) is True:
        return None
    with conn:
        conn.execute('insert into queue values (?,?)', (video_id,0,))


def mark_queue(video_id):
    with conn:
        conn.execute('update queue set processed = ? where id = ?', (1, video_id,))


def convert_subtitles():
    """
    convert vtt to srt for kodi
    """
    vtt_files = [i for i in os.listdir(video_dir) if i.endswith('vtt')]

    for i in vtt_files:
        os.rename(video_dir + i, subtitles + i)
        vtt_to_srt(subtitles + i)
        os.remove(subtitles + i)


def process_queue():
    while True:
        with conn:
            unprocessed = conn.execute('select id from queue where processed = 0')
            unprocessed = unprocessed.fetchone()
        if unprocessed is not None:
            unprocessed = unprocessed[0]
            get_video(unprocessed)
            mark_queue(unprocessed)
        convert_subtitles()

if __name__ == '__main__':
    process_queue()
