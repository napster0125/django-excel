#!/bin/bash

docker run --memory=256M --rm -v $PWD/app/media/:/app/media -it 'judge:latest' python3 run.py $1 $2 $3
