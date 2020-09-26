FROM python:3.8
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN wget http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz
RUN tar -xvf yasm-1.3.0.tar.gz && cd yasm-1.3.0 && ./configure && make && make install
RUN cd /code
RUN wget https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
RUN tar -xvf ffmpeg-snapshot.tar.bz2 && cd ffmpeg && ./configure && make && make install
COPY queue_processor.py .
COPY template.nfo .
CMD ["python3", "queue_processor.py"]
