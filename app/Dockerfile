FROM python:3.10.8-bullseye
RUN apt update && apt install ffmpeg libsm6 libxext6 -y

RUN addgroup --gid 1000 app_user && adduser --disabled-password --gecos '' --uid 1000 --gid 100 app_user
RUN mkdir /app && chown app_user:app_user /app
USER app_user

ADD ./requirements.txt /app/requirements.txt
RUN cd /app && pip install -r requirements.txt
ADD . /app
WORKDIR /app