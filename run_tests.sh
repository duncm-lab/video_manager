#!/usr/bin/env bash
find . -type f -name 'app.log' -exec rm -rf {} \;
coverage erase
python3 -m pylint --rcfile=.pylintrc app
python3 -m mypy --config-file .mypy.ini app
coverage run -m --source=app  unittest discover  ./app/tests
