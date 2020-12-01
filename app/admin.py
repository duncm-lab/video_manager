#!/usr/bin/env python3
# pylint: disable=all
from app.database import COLLECTION

videos = [(i['title'], i['_id']) for i in
          COLLECTION.find({}, {'title': True, '_id': True})]

for i in videos:
    print(i[1] + '~$' + i[0])
