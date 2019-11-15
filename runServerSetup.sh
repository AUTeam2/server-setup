#!/usr/bin/env bash
#
# Checks if user has installed Docker Toolbox or Desktop and
# Starts Application as appropriate

detectOStype(){
    if [[ `Uname` =~ "MING"? ]];then
      USER_OS="Windows"
    elif [[ `Uname` =~ "Darwin"? ]];then
      USER_OS="macOS"
    elif [[ `Uname` =~ "Linux"? ]];then
      USER_OS="Linux"
    else
      USER_OS="unknown"
    fi
    Printf "User OS is: %s \n" ${USER_OS}
}

getContainerStatus()
{
docker inspect --format '{{.State.Status}}' $1
}

getStatusForAll()
{
  STATUS_WEBINTERFACE_1="$(getContainerStatus server-setup_webinterface_1)"
  STATUS_NGINX_1="$(getContainerStatus server-setup_nginx_1)"
  STATUS_DB_1="$(getContainerStatus server-setup_db_1)"
  STATUS_MQTT_1="$(getContainerStatus server-setup_mqtt_1)"
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo "STATUS"
  echo ""
  echo "Webinterface = "${STATUS_WEBINTERFACE_1}""
  echo "nginx = "${STATUS_NGINX_1}""
  echo "DB = "${STATUS_DB_1}""
  echo "MQTT = "${STATUS_MQTT_1}""
  echo ""
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~"
}

dockerIsToolboxOrDesktop() {
  if [ "${DOCKER_TOOLBOX_INSTALL_PATH}" ];then
    echo "Using Docker Toolbox YML for Docker-Compose"
    DOCKER_COMPOSE_FILE=${DOCKER_TOOLBOX_YML}
  else
    dockerIsDesktop
  fi
}

dockerIsDesktop() 
{
  for d in "${PATH}"; do
    if [[ $d =~ "DockerDesktop"? ]]; then
        echo "Using Docker Desktop. Default YML chosen for Docker-Compose"
        DOCKER_COMPOSE_FILE=${DOCKER_DEFAULT_YML}
    else
        echo "Unable to detect Docker Installation, tries with Default YML"
    fi
  done
}

openServerPage()
{
    if [ "${USER_OS}" == "Windows" ];then
      start chrome ${URL}:${PORT}
    elif [ "${USER_OS}" == "macOS" ];then
      open "${URL}:${PORT}"
    elif [ "${USER_OS}" == "Linux" ];then
      xdg-open "${URL}:${PORT}"
    else
      echo "${USER_OS} OS, tries with windows settings to open browser"
      start chrome ${URL}:${PORT}
    fi
}

setURLForLocalOrServer() 
{
  if [ "${LOCAL_OR_SERVER}" == "team2" ];then
      echo "We are Running on the spooky team2 SERVER"
      URL=${SERVER_URL}
    else
      echo "We are Running LOCALLY. There is no place like home, cheers!"
      URL=${LOCAL_URL}
  fi
}

main (){

# Default Values
USER_OS="Doh! no OS Found"
LOCAL_OR_SERVER=whoami
DOCKER_DEFAULT_YML=docker-compose.yml
DOCKER_TOOLBOX_YML=docker-compose-win.yml
DOCKER_COMPOSE_FILE=${DOCKER_DEFAULT_YML}

 # Inet settings
LOCAL_URL=http://127.0.0.1
SERVER_URL=http://119.74.164.55
PORT=8000

# Set USER_OS to reflect actual OS on the Host machine and
# 
# Set URL to relfect server or local URL when opening browser
detectOStype
getStatusForAll
setURLForLocalOrServer
# Restart containers if they are running 
if [ "${STATUS_WEBINTERFACE_1}" == "running" ]; then
  echo "Wait a second..."
  echo "What a Mess we have here! 10's all over the place!"
  echo "Looks like we need to clean up and restart first!"
  docker-compose down
  docker volume rm data-volume
  docker volume rm mqtt-volume
fi

# If OS is Windows or "unknown" check whether Docker toolbox or
# Docker Desktop is installed to select Docker-Compose yml
if [ "${USER_OS}" == "Windows" ] || [ "${USER_OS}" == "unknown"  ]; then
    dockerIsToolboxOrDesktop
fi

# Link to required Sorce files
echo "OK! Everything is ready to be started now!"
echo Sourced from: https://github.com/AUTeam2/server-setup
echo "Creates the docker required docker Volumes"
docker volume create data-volume
docker volume create mqtt-volume

echo "Builds the images as needed"
docker-compose build

echo "Lists created images"
docker-compose images

echo "Starts the application in docker containers"
docker-compose -f ${DOCKER_COMPOSE_FILE} up -d

getStatusForAll
# Opens server or localhost in browser
sleep 5.0
openServerPage

echo "------------END------------"
}

# Run Main sequence
main