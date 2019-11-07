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

The containers are shut down using `docker-compose down`. 

## Creating volumes

To make data persistent outside the Docker container, we use volumes. This is essentially just attached storage. 
To make the needed volumes:
- for the database, run `docker volume create data-volume`
- for the mosquitto server, run `docker volume create mqtt-volume`
