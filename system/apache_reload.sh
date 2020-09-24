#!/usr/bin/env sh

site_name=video
site_url=http://localhost:8081/video

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
