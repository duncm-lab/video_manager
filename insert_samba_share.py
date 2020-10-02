#!/usr/bin/env python3
"""
Return a share entry for a samba share to be inserted in smb.conf

[name]
wide links = yes
follow symlinks = yes
comment = name
browseable = yes
path = BASE_PATH + name
guest ok = yes
read only = yes
create mask = 0700

"""
import sys
from string import Template
from app.config import BASE_PATH

samba_template = Template('[$name]\n \
    wide links = yes\n \
    follow symlinks = yes\n \
    comment = $name\n \
    browseable = yes\n \
    path = $path$name\n \
    guest ok = yes\n \
    read only = yes\n \
    create mask = 0700')

if __name__ == '__main__':
    t = samba_template.substitute(name=sys.argv[1], path=BASE_PATH)
    print(t)
