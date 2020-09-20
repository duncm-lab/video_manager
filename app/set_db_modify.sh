#!/usr/bin/env bash

if [ "$1" == "on" ]; then
    chown ubuntu:ubuntu video_db/
    chown ubuntu:ubuntu video_db/queue.db
else
    chown www-data:www-data video_db/
    chown www-data:www-data video_db/queue.db
fi
