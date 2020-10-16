FROM ubuntu:latest
# shell scripts for setting up packages and other assorted dependencies
WORKDIR /code
COPY environment_setup.sh .
RUN ls
RUN chmod +x environment_setup.sh
RUN ./environment_setup.sh
#install app dependencies from pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
#force a copy from host and not cache
ARG CACHE_DATE=not_a_date
#copy application files into container
COPY app/config.py app/config.py
COPY app/database.py app/database.py
COPY app/queue_processor/template.nfo app/queue_processor/template.nfo
COPY app/queue_processor/queue_processor.py app/queue_processor/queue_processor.py
COPY app/sync_video/add_to_queue.py app/sync_video/add_to_queue.py
COPY app/sync_video/sync_video.py app/sync_video/sync_video.py
#expose ports for communication with the outside world
#link container directories with host directories for data persistance
VOLUME /mnt/files/data/logs:/logs
VOLUME /mnt/files/data/mongo:/data/db
VOLUME /mnt/files/share/video:/mnt/files/share/video
# application start
COPY main.sh .
RUN chmod +x main.sh
CMD "./main.sh"
