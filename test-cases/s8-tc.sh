#!/usr/bin/env bash

# This script runs test cases S8.TC-1, TC-2, TC-3 and TC-4
# Only tested on MacOS so far.
# I don't think TC-4 is compatible on Windows, and I am not sure about the utils to use for windows to replace nc and grep...
# Janus 21 Nov 2019

MQTT_PORT="8000"
WEBSOCK_PORT="8081"
URL="auteam2.mooo.com"
TMP_FILE="./test-cases/s8-tc-tmp.txt"
TEST_MSG="This is a test message sent from publisher to subscriber via the server."

# Attempting to determine the system, and set the correct commands
# Prepare
if [[ "$(uname)" =~ "MING"? ]];then
  USER_OS="Windows"
  DOCKERCOMPOSEUP="docker-compose -f docker-compose-win.yml up -d --build"
  LOCALHOST="192.168.99.100"
  PORTSCANNER="nc -z"
  WORDSEARCH="grep -w"

elif [[ "$(uname)" =~ "Darwin"? ]];then
  USER_OS="macOS"
  DOCKERCOMPOSEUP="docker-compose up -d --build"
  LOCALHOST="localhost"
  PORTSCANNER="nc -z"
  WORDSEARCH="grep -w"

elif [[ "$(uname)" =~ "Linux"? ]];then
  USER_OS="Linux"
  DOCKERCOMPOSEUP="docker-compose up -d --build"
  LOCALHOST="localhost"
  PORTSCANNER="nc -z"
  WORDSEARCH="grep -w"

else
  USER_OS="unknown"
  DOCKERCOMPOSEUP="docker-compose up -d --build"
  LOCALHOST="localhost"
  PORTSCANNER="nc -z"
  WORDSEARCH="grep -w"

fi

service_running () {
  if [[ -z "$(docker-compose ps | ${WORDSEARCH} ".*mqtt.*Up.*")" ]]; then
    false # the service mqtt does not have Up in the status
  else
    true
  fi
}

listening_on () {
  if [[ -z "$( ${PORTSCANNER} "$1" "$2" 2>&1 | ${WORDSEARCH} "succeeded" )" ]]; then
    false #the word succeeded was not found, so the service is not listening on the specified URL and PORT
  else
    true
  fi
}

get_credentials () {
  if [[ -z "${MOSQUITTO_USER}" ]] || [[ -z "${MOSQUITTO_PASSWORD}" ]]; then
    echo "Enter credentials for the Mosquitto server:"
    read -p "Enter User: " MOSQUITTO_USER
    read -s -p "Enter Password: " MOSQUITTO_PASSWORD
    echo ""
    export MOSQUITTO_USER
    export MOSQUITTO_PASSWORD
  fi
}



#Font colours
RED='\033[1;31m'         # Bold red
GREEN='\033[0;32m'       # Bold green
YELLOW='\033[0;33m'      # Bold yellow
HEAD='\033[1;37;44m'
NC='\033[0m' # No Color

#### Info to users ###
echo -e "${HEAD}Running all testcases for deliverable S8${NC}"

#### TEST-CASE TC-1 ####
TC="S8.TC-1"
echo -e "${HEAD}*** Test-case ${TC} ***${NC}"
echo "Verifies that the Mosquitto server is successfully running in docker-compose"

if service_running; then
  echo -e "${TC}: ${GREEN}OK${NC}. Service is running."
else
  echo -e "${YELLOW}Service not started${NC}. Attempting to build and start."
  $DOCKERCOMPOSEUP

  if service_running; then
    echo -e "${TC}: ${GREEN}OK${NC}. Service is running."
  else
    echo -e "${TC}: ${RED}FAILED${NC}. Service could not be started."
    exit 1
  fi
fi

#### TEST-CASE TC-2.01 ####
TC="S8.TC-2.01"
echo -e "${HEAD}*** Test-case ${TC} ***${NC}"
echo "Verifies that the Mosquitto-server is listening on ${LOCALHOST} ports ${MQTT_PORT} and ${WEBSOCK_PORT}."

if listening_on "${LOCALHOST}" "${MQTT_PORT}"  && listening_on "${LOCALHOST}" "${WEBSOCK_PORT}" ; then
  echo -e "${TC}: ${GREEN}OK${NC}. Service is listening."
else
  echo -e "${TC}: ${RED}FAILED${NC}. Service is not listening."
fi

#### TEST-CASE TC-2.02 ####
TC="S8.TC-2.02"
echo -e "${HEAD}*** Test-case ${TC} ***${NC}"
echo "Verifies that the Mosquitto-server is listening on ${URL} ports ${MQTT_PORT} and ${WEBSOCK_PORT}."

if listening_on "${URL}" "${MQTT_PORT}"  && listening_on "${URL}" "${WEBSOCK_PORT}" ; then
  echo -e "${TC}: ${GREEN}OK${NC}. Service is listening."
else
  echo -e "${TC}: ${RED}FAILED${NC}. Service is not listening."
fi



#### TEST-CASE TC-3 ####
TC="S8.TC-3"
echo -e "${HEAD}*** Test-case ${TC} ***${NC}"
echo "Verifies that a message can be sent to the Mosquitto server on $LOCALHOST port $MQTT_PORT."

# Ask and set credentials if not inherited from parent process
get_credentials
if mosquitto_pub -h ${LOCALHOST} -p ${MQTT_PORT} -t "Test/topic" -m "Test message" --id TestPublisher -u "${MOSQUITTO_USER}" -P "${MOSQUITTO_PASSWORD}"; then
  echo -e "${TC}: ${GREEN}OK${NC}. Service can accept publish messages."
else
  echo -e "${TC}: ${RED}FAILED${NC}. Service declined the operation."
fi


#### TEST-CASE TC-4 ####
TC="S8.TC-4"
echo -e "${HEAD}*** Test-case ${TC} ***${NC}"
echo "Verifies that a topic can be subscribed to and that a message can received from the Mosquitto server on $LOCALHOST port $MQTT_PORT."
get_credentials

# Start the subscriber as a background process and direct the output to a file
mosquitto_sub -h ${LOCALHOST} -p ${MQTT_PORT} -t "Test/topic" --id TestSubscriber -u "${MOSQUITTO_USER}" -P "${MOSQUITTO_PASSWORD}" > "${TMP_FILE}" & PROC_ID=$!
disown
sleep 1 # Wait to ensure it's running

# Send a publish message
mosquitto_pub -h ${LOCALHOST} -p ${MQTT_PORT} -t "Test/topic" -m "${TEST_MSG}" --id TestPublisher -u "${MOSQUITTO_USER}" -P "${MOSQUITTO_PASSWORD}"

# Wait for message handling, kill the subscribe process
sleep 1
kill -1 ${PROC_ID} 2>/dev/null

# Read back the output from the received message and compare to what was sent
RCV_MSG=$(tr -d '\0' < $TMP_FILE )
if [ "${RCV_MSG}" = "${TEST_MSG}" ]; then
  echo "Received the message: ${RCV_MSG}"
  echo -e "${TC}: ${GREEN}OK${NC}. Messages on subscribed topics can be received from the service."
else
  echo -e "${TC}: ${RED}FAILED${NC}. Nothing received or mismatch."
fi

rm "${TMP_FILE}"

echo -e "${HEAD}Testcases done.${NC}"
