# Webinterface application folder

This folder contains files needed to run the Webinterface application code.

## Dockerfile
The Dockerfile specifies the image we use to run Django. It contains the further setup of the base image to make it usable for us.

## requirements.txt
Contains all Python packages that are required to run the Webinterface application. Add packages here, if additional Python functionality is required.

## Entrypoint.sh
This script is triggered every time the container starts up.
It ensures that the database server (from another container) is running before starting Django. 
The reason: We ask Django to perform all database migrations on startup, and these of course require database access.
