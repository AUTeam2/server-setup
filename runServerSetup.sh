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

main (){

# Default Values
USER_OS="Doh! no OS Found"
DOCKER_DEFAULT_YML=docker-compose.yml
DOCKER_TOOLBOX_YML=docker-compose-win.yml
DOCKER_COMPOSE_FILE=${DOCKER_DEFAULT_YML}
URL=127.0.0.1
PORT=8000

# Set USER_OS to reflect actual OS on the Host machine
detectOStype

# If OS is Windows or "unknown" check whether Docker toolbox or
# Docker Desktop is installed to select Docker-Compose yml
if [ "${USER_OS}" == "Windows" ] || [ "${USER_OS}" == "unknown"  ]; then
    dockerIsToolboxOrDesktop
fi

# Link to required Sorce files
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
echo "------------END------------"

# Opens 127.0.0.1:8000 (localhost) in a browser
sleep 5.0
openServerPage
}

# Run Main sequence
main