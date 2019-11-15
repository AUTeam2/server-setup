#!/usr/bin/env bash

# This file is ONLY for bootstrapping the first project!
# That means: NO ./webinterface/manage.py and NO ./webinterface/webinterface/
# Run it multiple times at your own risk :)

# Make a docker volume for the database
docker volume create data-volume

# Make a docker volume for the Mosquitto server
docker volume create mqtt-volume

# Build the containers
docker-compose build

# Create the Django project files
docker-compose run webinterface sh -c "django-admin.py startproject webinterface ."

# Start up the services
docker-compose up -d --build

# Migrate the database for the new project
docker-compose exec webinterface python manage.py migrate --noinput

# Create a superuser for the admin role
docker-compose exec webinterface python manage.py createsuperuser --username ditnavn --email dit@navn.dk
