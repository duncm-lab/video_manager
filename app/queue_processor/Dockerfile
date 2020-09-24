FROM python:3.8
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY queue_processor.py .
COPY template.nfo .
VOLUME ["/mnt/files/share/video/"]
RUN ["python3", "queue_processor.py", "&"]
