# Webinterface application folder

This folder contains files needed to run the Webinterface application code.

## TO DO:
- [ ] Modify the Django settings to use the Postgres database
- [ ] Modify the Django settings to use the Nginx server via WSGI middleware
- [ ] Move secret keys out for production, ensure Django environment has username and password for the database

## Dockerfile
The Dockerfile specifies the image we use to run Django. It contains the further setup of the base image to make it usable for us.

## requirements.txt
Contains all Python packages that are required to run the Webinterface application. Add packages here, if additional Python functionality is required.

## entrypoint.sh
This script is triggered every time the container starts up.
It ensures that the database server (from another container) is running before starting Django. 
The reason: We ask Django to perform all database migrations on startup, and these of course require database access.

## webinterface
Contains the base Django files for the Webinterface
