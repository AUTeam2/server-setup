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

# To make migrations for any newly added models -- don't do that here first...
# Run something like: docker-compose exec webinterface python manage.py makemigrations database_poc

#Migrating newly added models
# python manage.py makemigrations

#Migrate performs all database migrations that are already prepared
python manage.py migrate

#Collect all static files (images, sound, etc.) into staticfiles-folder to be served by Nginx
python manage.py collectstatic --no-input --clear

#Add tasks to the crontab scheduler
python manage.py crontab add

echo "Waiting for MQTT service before starting Message Handler"

#Use netcat to scan for daemons, we wait until our MQTT service is running
#while ! nc -z mqtt 8000; do
#  sleep 0.1
#done

echo "MQTT started... Starting Message Handler"

#python manage.py start_messagehandler

#Expand all positional arguments to this script and execute them, hand over control
exec "$@"
