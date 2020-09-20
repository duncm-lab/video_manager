#!/usr/bin/env sh

web_folder=/srv/video
project_folder=/home/ubuntu/code/video
site_name=video
site_url=http://localhost:8081/video

if [ -d "$web_folder" ]; then
    rm -rf "$web_folder"
fi

mkdir $web_folder

cp -r sync_video.py $web_folder
cp -r add_to_queue.py $web_folder


chown -R www-data:www-data $web_folder
chmod -R u+rw $web_folder
chmod -R o+rw $web_folder

a2dissite $site_name
service apache2 reload
a2ensite $site_name
service apache2 reload

test_response=`curl -sX GET $site_url | grep -i "200"`

if [ -z $test_response ]; then
    echo "failed"
    tail -15 /var/log/apache2/error.log
else
    echo "pass"
fi
