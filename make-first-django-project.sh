#!/usr/bin/env bash

# Make a docker volume for the database
docker volume create data-volume

# Build and start the containers
docker-compose up --build

# Create the project
docker-compose exec webinterface django-admin.py startproject webinterface .

# Migrate the database for the new app
docker-compose exec webinterface python manage.py migrate --noinput

# Create a superuser for the admin role
docker-compose exec webinterface python manage.py createsuperuser --username admin --email test@test.dk
