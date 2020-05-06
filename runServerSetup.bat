start /
:: Link to required Sorce files
echo Sourced from: https://github.com/AUTeam2/server-setup

:: Creates the Docker required docker Volumes
docker volume create data-volume
docker volume create mqtt-volume

:: builds the iamges if as needed
docker-compose build

:: Lists created images
docker-compose images

:: Starts the application in docker containers
docker-compose -f docker-compose.yml up -d

echo Server should be up in a moment!

SLEEP 5

start chrome http://localhost:8001

Echo closing prompt

SLEEP 3