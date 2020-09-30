#set base image
FROM python:3.8-alpine
#set the container working directory
WORKDIR /code
#copy dependencies list
COPY requirements.txt .
#install dependencies
RUN pip install -r requirements.txt
#copy modules to working dir
COPY add_to_queue.py .
COPY sync_video.py .
ENV FLASK_APP sync_video.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 8080
#run program
CMD ["flask", "run", "--port=8080"]
