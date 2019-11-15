#!/usr/bin/env bash

# Make a docker volume for the database
docker volume create data-volume

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
