#!/usr/bin/env python3
import sqlite3
import sys

conn = sqlite3.connect('/home/pi/code/videos.db', check_same_thread=False)
with conn as db:
    cur = db.cursor()
    cur.execute('update video set processed = 1 where id = ?', (sys.argv[1],))
