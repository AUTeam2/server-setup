# Containerized server setup for Pro3 and Pro4

This repo contains files for setting up all needed server services for the Web interface for Pro3 and Pro4.

## Services

The docker-compose now contains the following services:
- PostgreSQL database server
- Mosquitto server

## How to use

The *docker-compose.yml* file coordinates startup and shutdown of the containers, and ensures a network between running containers. The file also opens and maps certain ports to the host OS. It also specifies storage.

Before running the containers the first time, see the sections [Creating volumes](#Creating-volumes) and [Building Webinterface image](#Building-Webinterface-image)..

The containers are started using `docker-compose up -d`. The `-d` options start the containers in a detached state, i.e. running in the background.

If you want to see console and log output from the containers, run in foreground as `docker-compose up`

The containers are shut down using `docker-compose down`. If running in the foreground, stop them using *Ctrl-C*.

## Creating volumes

To make data persistent outside the Docker container, we use volumes. This is essentially just attached storage. 
To make the needed volumes:
- for the database, run `docker volume create data-volume`
- for the mosquitto server, run `docker volume create mqtt-volume`

## Building Webinterface image

The first build of the Webinterface image takes a while, because many different libraries must be fetched and installed.

To build the image without starting it, go to the webinterface folder `cd webinterface` and run `docker build .`.

## Issuing command line commands to the Webinterface

Any command line command can be issued to the Webinterface container like `docker-compose run webinterface sh -c "django-admin.py startproject webinterface ."`

The command in the example starts a new Django project called webinterface.

## Development Server

The current setup runs Django via its own development server. Later, we connect Django and Nginx via a gateway interface (WSGI). I propose using gunicorn.

