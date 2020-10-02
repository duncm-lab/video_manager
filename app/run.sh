#!/usr/bin/env bash

#call various setup scripts and start the app

./sync_config.sh
sudo docker-compose up --build -d --remove-orphans
