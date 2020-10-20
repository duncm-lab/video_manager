#!/usr/bin/env bash
python3 -m pylint app
python3 -m mypy app
python3 -m nose app
