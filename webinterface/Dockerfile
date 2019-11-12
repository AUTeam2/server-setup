#Pull image for Linux Alpine with Python 3.8
FROM python:3.8.0-alpine
MAINTAINER Team Web, Janus Bo Andersen

#Set the working directory inside the Alpine Container
WORKDIR /usr/src/webinterface

#Set environment variables
#don't write .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
#don't buffer stdout, as that causes errors
ENV PYTHONUNBUFFERED 1

#Install dependencies for PostgreSQL (Psycopg2)
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

#Install dependencies inside container
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/webinterface/requirements.txt
RUN pip install -r requirements.txt

#Copy the entry point file
COPY ./entrypoint.sh /usr/src/webinterface/entrypoint.sh

#Copy all project files (Later: set up an auto sync)
COPY . /usr/src/webinterface/

RUN chmod 777 /usr/src/webinterface/entrypoint.sh

#Create a user to avoid running as root
#RUN adduser -D nonrootuser
#USER nonrootuser

#Run entrypoint, positional arguments can be added later
ENTRYPOINT ["/usr/src/webinterface/entrypoint.sh"]
