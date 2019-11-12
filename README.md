# Containerized server setup for Pro3 and Pro4 :rocket:

This repo contains files for setting up all needed server services for the Web interface for Pro3 and Pro4.

## TO DO:
- [ ] Test Windows comaptibility of custom Python/Django image.
- [ ] Connect Nginx webserver with Django through gunicorn.

## Services
The docker-compose now contains the following services:
- PostgreSQL database server
- Mosquitto server
- Django webinterface, hosted by a development server
- Nginx webserver

## Docker-compose
The *docker-compose.yml* file handles:
- Coordination of construction, startup, shutdown and destruction of the services (running in containers).
- Creation of networking bridges between running services (between containers). 
- Mapping of ports between containers and the host OS.
- Specification of storage volumes and mapping to local folders.

## How to use
Before running the services the first time, see the sections:
- [Creating volumes](#Creating-volumes).
- [Building Webinterface image](#Building-the-Webinterface-image).

The services are created using `docker-compose up -d`. The `-d` options creates the services in a detached state, i.e. running in the background.

If you want to see console and log output from the services, run in foreground as `docker-compose up`

The containers are destroyed using `docker-compose down`. If running in the foreground, stop them using *Ctrl-C*.

## Creating and destroying versus starting and stopping
Services that are already built can be started and stopped without re-building, using `docker-compose start` and `docker-compose stop`. This is good for production, but if you change the build instructions, you are not guaranteed that your changes are included in the running services.

The calls `docker-compose up -d` and `docker-compose down` re-build and destroy containers at each run, which is good during development, ensuring that all changes are captured in the services.

To see the built images on your computer, run `docker-compose images`

## Creating volumes
To make data persistent outside the Docker container, we use volumes. This is essentially just attached storage. 
To make the needed volumes:
- for the database, run `docker volume create data-volume`
- for the mosquitto server, run `docker volume create mqtt-volume`

## Building the Webinterface image
The first build of the Webinterface image takes a while, because many different libraries must be fetched and installed.
To build all the images for all services in the docker-compose, without starting them, run `docker-compose build`.

## Issuing command line commands to the Webinterface
Any command line command can be issued to the Webinterface container like `docker-compose run webinterface sh -c "django-admin.py startproject webinterface ."`

The command in the example starts a new Django project called webinterface.

## Development server
The current service setup runs Django hosted on its own development server. This server is unsafe, insecure, slow and doesn't handle multiple concurrent connections. Later, we will connect Django and Nginx via a gateway interface (WSGI). I propose using gunicorn.

## Running on Windows with Docker Toolbox
To start the containers on Windows, use the `docker-compose-win.yml` file, running it as `docker-compose -f docker-compose-win.yml up -d`.

To share local files with the container (config files, etc.), you must set up a shared folder in Virtual Box:
- The folder **server-settings** (this repository) must be shared with the Docker Toolbox.
- The name of the shared folder _must_ be `c/Docker`.

:rocket:
