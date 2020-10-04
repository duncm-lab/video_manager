#!/usr/bin/env bash
# setup environment and install packages

apt-get update && apt-get install -y \
        software-properties-common
add-apt-repository universe
apt-get update && apt-get install -y \
        python3-pip
apt-get install -y ffmpeg
apt-get install -y curl
apt-get install -y vim
