[![Build Status](https://travis-ci.org/duncm-lab/video_manager.svg?branch=main)](https://travis-ci.org/duncm-lab/video_manager)

# Features

+ Download youtube videos to a specified location
+ Create nfo file for kodi
+ Create thumbnails for kodi

Download youtube videos, create .nfo and thumbnail files for kodi and
automatically specify the location on disk to store to.


# Requirements
+ Docker


# Installation

1. git clone https://github.com/duncm-lab/video\_manager.git
2. cd video\_manager
3. sudo docker-compose -up -d (or you can have you console blocked :-) )




# Configuration
Files found in project root directory


## docker-compose.yml
Probably a few things you'll want to change here


### services
+ mongo
    - volumes
+ mongo-express (not needed but useful, remove if you wish)
    - ports
+ app
    - volumes


## Dockerfile
Update the VOLUMES in the Dockerfile to match any changes in compose


# Overview
The main modules in the app are sync\_video and queue\_processor.
When a request is made to /Sync/video\_id/some,tags a document
is created in the database with the metadata of the video.

queue\_processor then does the following:
    1. convert the tags key to a folder path e.g. ['sports', 'ball']
    becomes VIDEO_DIR/sports/ball
    2. A folder is created based on title of the video within the
    aforementioned folder
    3. youtube\_dl is called to download the video
    4. tvshow.nfo is created based on the metadata in the database
    5. thumbnail.jpg is downloaded
