#!/bin/sh

# We use this entrypoint script to check if Postgres is running and then performing django migrations

echo "Waiting for postgres..."

#Use netcat to scan for daemons, we wait until our db service is running
while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

#Perform Django action

#Flush clears the DB
#python manage.py flush --no-input

#Migrate performs all database migrations
python manage.py migrate

#Expand all positional arguments to this script and execute them
exec "$@"
