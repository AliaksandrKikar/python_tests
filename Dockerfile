FROM jenkins/jenkins:lts-jdk11
USER root
RUN mkdir /my_app
WORKDIR /my_app
COPY main.py /my_app
RUN apt update
RUN apt install -y python3