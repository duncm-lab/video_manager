#!/usr/bin/env bash

pgrep -f "queue_processor|flask" && pgrep -f "queue_processor|flask" | xargs kill -9
ls | grep -i "nohup.out" && rm nohup.out
nohup python3 app/queue_processor/queue_processor.py &
export FLASK_APP=app/sync_video/sync_video
flask run --host=0.0.0.0
