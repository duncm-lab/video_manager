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
COPY app/*.py app/
COPY app/*.yml app/
COPY app/sync_video/ app/sync_video/
COPY app/queue_processor/ app/queue_processor/

#expose ports for communication with the outside world
#link container directories with host directories for data persistance
VOLUME /mnt/files/data/logs:/logs #app
VOLUME /mnt/files/data/mongo:/data/db #mongo
VOLUME /mnt/files/share/video:/mnt/files/share/video #app
# application start
COPY main.sh .
RUN chmod +x main.sh
CMD "./main.sh"
