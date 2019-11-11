# Containerized server setup for Pro3 and Pro4

This repo contains files for setting up all needed server services for the Web interface for Pro3 and Pro4.

## Services

The docker-compose now contains the following services:
- PostgreSQL database server
- Mosquitto server

## How to use

The *docker-compose.yml* file coordinates startup and shutdown of the containers, and ensures a network between running containers. The file also opens and maps certain ports to the host OS. It also specifies storage.

Before running the containers the first time, see the section [Creating volumes](#Creating-volumes).

The containers are started using `docker-compose up -d`. The `-d` options start the containers in a detached state, i.e. running in the background.

If you want to see console and log output from the containers, run in foreground as `docker-compose up`

The containers are shut down using `docker-compose down`. If running in the foreground, stop them using *Ctrl-C*.

## Creating volumes

To make data persistent outside the Docker container, we use volumes. This is essentially just attached storage. 
To make the needed volumes:
- for the database, run `docker volume create data-volume`
- for the mosquitto server, run `docker volume create mqtt-volume`


## Running on Windows with Docker Toolbox

To start the containers on Windows, use the `docker-compose-win.yml` file, running it as `docker-compose -f docker-compose-win.yml up -d`.

To share local files with the container (config files, etc.), you must set up a shared folder in Virtual Box:
- The folder **server-settings** (this repository) must be shared with the Docker Toolbox.
- The name of the shared folder _must_ be `c/Docker`.
