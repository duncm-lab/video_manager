#!/usr/bin/env bash
find . -type f -name 'app.log' -exec rm -rf {} \;
sed -i 's/video_dir: .*$/video_dir: .\//g' ./app/config.yml #dirty hack for now
coverage erase
python3 -m pylint --rcfile=.pylintrc app
python3 -m mypy --config-file .mypy.ini app
coverage run -m --source=app  unittest  discover -v  ./app/tests
sed -i 's/video_dir: .*$/video_dir: \/mnt\/files\/share\/video\//g' ./app/config.yml
