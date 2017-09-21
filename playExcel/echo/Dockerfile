FROM alpine

RUN apk add --update bash
RUN apk add --update python3
RUN apk add --update mkvtoolnix
RUN apk add --update curl

ENV PATH="${PATH}:/media/programs"

RUN ln -s /bin/bash /bin/rbash
RUN rm -rf /var/cache/apk/*
RUN rm -rf /bin/dd /bin/mount /bin/mountpoint /bin/pwd /bin/rm /bin/rmdir /bin/uname /bin/sleep /bin/ping
