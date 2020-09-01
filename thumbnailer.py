import os
import subprocess
from string import Template

kodi_host = 'root@192.168.1.232'
smb_url = 'smb://192.168.1.135/videos' 

#get the files from the video dir
file_dicts = [{os.path.split(i[0])[1]: i[2]} for i in os.walk('/home/ubuntu/video')][1:]


def remote_query(sql):
    print(sql)
    subprocess.run(['ssh', kodi_host, 'sqlite3', 
        '/storage/.kodi/userdata/Database/Textures13.db',
        "\"{}\"".format(sql)])

staging = []
#strip out un-needed files
for i in file_dicts:
    for key, values in i.items():
        folder_path = smb_url + '/' + key
        video_file = folder_path + '/' + [v for v in values 
                if v not in ['tvshow.nfo', 'thumbnail.jpg']][0]
        staging.append({'folder': folder_path + '/',
            'video': video_file,
            'thumbnail': folder_path + '/' + 'thumbnail.jpg'}) 


remote_query('delete from path;')


with open('add_images_template.sql', 'r') as fl:
    sql_template = Template(fl.read())

for i in staging:
    sql = sql_template.substitute(folderurl=i['folder'],
            videourl=i['video'],
            texture=i['thumbnail'])
    remote_query(sql)
