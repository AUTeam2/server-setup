# Container setup for Pro3 and Pro4

This repo contains files for setting up all needed server services for the Web interface for Pro3 and Pro4.

## How to use

The Docker-compose.yml file coordinates startup and shutdown of the containers, and ensures a network between running containers.

The containers are started using `docker-compose up -d` (the `-d` options start the containers in a detached state (running in the background).
The containers are shut down using `docker-compose down`. 

## Services

The docker-compose contains the following services
- PostgreSQL database
- Mosquitto server

## Volumes

To make data persistent outside the Docker container, we use a Volume. It is essentially just attached storage. 
To make the needed volume for the database, run `docker volume create data-volume`.
To make the needed volume for the mosquitto server run `docker volume create mosquitto-volume`.
