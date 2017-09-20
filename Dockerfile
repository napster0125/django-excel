FROM ubuntu:latest

MAINTAINER Siva R "sivagrenganathan@gmail.com"

# INSTALL COMPILERS
RUN apt-get update && apt-get install -y \
  openjdk-8-jdk \
  g++ \
  python \
  python3 \
  python3-pip

COPY playexcel/app/. /app/

WORKDIR /app/
