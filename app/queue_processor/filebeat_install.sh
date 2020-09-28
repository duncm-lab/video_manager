#!/usr/bin/env bash

#bash script for filebeat install
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.7.0-amd64.deb
dpkg -i filebeat-7.7.0-amd64.deb
