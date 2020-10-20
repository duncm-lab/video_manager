[![Build Status](https://travis-ci.org/duncm-lab/video_manager.svg?branch=main)](https://travis-ci.org/duncm-lab/video_manager)

# Features

+ Download youtube and categories youtube videos by calling a URL endpoint e.g.
/Sync/video\_id
+ Create nfo files for Kodi
+ Create thumbnails for kodi


# Requirements
+ Docker


# Installation

1. git clone https://github.com/duncm-lab/video\_manager.git
2. cd video\_manager
3. sudo docker-compose -up -d (or you can have you console blocked :-) )

# Usage

curl -X GET http://your-hostname:8080/Sync/video\_id/some,tags

# Endpoint

