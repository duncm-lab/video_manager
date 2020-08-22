#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('/home/pi/code/video/video_db/queue.db', check_same_thread=False)

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
