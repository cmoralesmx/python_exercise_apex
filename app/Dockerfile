FROM python:3.10.8-bullseye
RUN apt update && apt install ffmpeg libsm6 libxext6 -y
ADD . /app
RUN cd /app && pip install -r requirements.txt
WORKDIR /app