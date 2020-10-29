#!/usr/bin/env bash

pgrep -f "queue_processor|flask" && pgrep -f "queue_processor|flask" | xargs kill -9
# shellcheck disable=SC2010
ls | grep -i "nohup.out" && rm nohup.out
export PYTHONPATH=./
nohup python3 app/queue_processor/queue_processor.py &
export FLASK_APP=app/sync_video/sync_video
flask run --host=0.0.0.0 --port=8080
