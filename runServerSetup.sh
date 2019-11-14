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


main (){

# Default Values
USER_OS="Doh! no OS Found"
DOCKER_DEFAULT_YML=docker-compose.yml
DOCKER_TOOLBOX_YML=docker-compose-win.yml
DOCKER_COMPOSE_FILE=${DOCKER_DEFAULT_YML}

# Set USER_OS to reflect actual OS on the Host machine
detectOStype

# If OS is Windows check whether Docker toolbox or
# Docker Desktop is installed to select Docker-Compose yml
if [ "${USER_OS}" == "Windows" ]; then
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

}

# Run Main sequence
main