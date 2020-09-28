#set base image
FROM python:latest
#set the container working directory
WORKDIR /code
#copy dependencies list
COPY requirements.txt .
#install dependencies
RUN pip install -r requirements.txt
#copy modules to working dir
COPY add_to_queue.py .
COPY sync_video.py .
#run program
CMD ["python3", "sync_video.py"]
