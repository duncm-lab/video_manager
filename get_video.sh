#!/usr/bin/env sh


for i in "`cat ~/code/video/videos.txt`"
do
    youtube-dl $i
done
