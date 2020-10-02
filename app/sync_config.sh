#!/usr/bin/env bash

# copy the app/config.py and app/database.py file into each of the service folders


cp -f config.py ./sync_video/
cp -f config.py ./queue_processor/
cp -f database.py ./sync_video/
cp -f database.py ./queue_processor/
