FROM ubuntu:latest

MAINTAINER Siva R "sivagrenganathan@gmail.com"

# INSTALL COMPILERS
RUN apt-get update && apt-get install -y \
  openjdk-8-jdk \
  g++ \
  python \
  python3 \
  python3-pip

COPY requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt

COPY app/. /app/

WORKDIR /app/
