#!/bin/bash

if [ "$1" != "True" ]; then
    docker run --rm -v $PWD/echo/media:/media -w /media 'echojudge:latest' python3 judge.py $2 $3 "$4" $5 $6
else
    docker run --rm -v $PWD/echo/media:/media -w /media/players/$2/home/level$3 'echojudge:latest' rbash -c "$4"
fi