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
COPY filebeat_install.sh .
RUN ./filebeat_install.sh
COPY queue_processor.py .
COPY template.nfo .
CMD ["python3", "queue_processor.py"]
