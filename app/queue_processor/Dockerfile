FROM ubuntu:latest
WORKDIR /code
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
        software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
        python3-pip
RUN pip3 install -r requirements.txt
RUN apt-get install -y ffmpeg
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.9.2-amd64.deb
RUN dpkg -i filebeat-7.9.2-amd64.deb
COPY ./filebeat_config/filebeat.yml /etc/filebeat/filebeat.yml
#RUN filebeat modules enable system
#COPY ./filebeat_config/system.yml /ect/filebeat/modules.d/system.yml
#RUN filebeat setup -e
#RUN service filebeat start
COPY config.py .
COPY queue_processor.py .
COPY template.nfo .
CMD ["python3", "queue_processor.py"]
