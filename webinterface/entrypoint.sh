#!/bin/sh

# We use this entrypoint script to check if Postgres is running and then performing django migrations
echo "Waiting for PostgreSQL service before starting Django..."

#Use netcat to scan for daemons, we wait until our db service is running
while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started... Starting Django now."

#Perform Django actions

#Flush clears the DB, good if you want to start from fresh for some reason
#python manage.py flush --no-input

#Adding crontab scheduler
python manage.py crontab add

#Migrating newly added models
#python manage.py makemigrations

#Migrate performs all database migrations
python manage.py migrate

#Running the Django server
#python manage.py runserver

#Expand all positional arguments to this script and execute them, hand over control
exec "$@"
