#!/usr/bin/env bash


youtube-dl --get-id -e --get-duration "ytsearch$2:$1" | split -l3
date 
for i in `ls xa*`
do
     row=`tr '\n', '|' < $i`
     echo $1"|"$row | column -t -s '|'
done


rm xa*
