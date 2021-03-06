FROM python:3.7-alpine
MAINTAINER AnsumanSingh@perplexsolutions.com

ENV PYTHONUNBUFFERED 1

RUN echo http://nl.alpinelinux.org/alpine/v3.9/main > /etc/apk/repositories; \
    echo http://nl.alpinelinux.org/alpine/v3.9/community >> /etc/apk/repositories

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-debs \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-debs

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D ansuman
USER ansuman


