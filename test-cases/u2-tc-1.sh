echo "Running testcase: U2.TC-1"
echo "Verifikation af at Django på Docker fungerer på lokalmaskine"
echo "Linux og Mac"

URL=http://localhost
URL_WIN=http://192.168.99.100
PORT=8001

# Prepare
if [[ `uname` =~ "MING"? ]];then
  USER_OS="Windows"
elif [[ `uname` =~ "Darwin"? ]];then
  USER_OS="macOS"
elif [[ `uname` =~ "Linux"? ]];then
  USER_OS="Linux"
else
  USER_OS="unknown"
fi

# Set up to ensure fresh start
docker-compose down
docker volume rm data-volume
docker volume rm mqtt-volume
docker volume create data-volume
docker volume create mqtt-volume

# Get updated code from relevant branch
# git pull
# git checkout master

# Perform test steps
echo "*** TEST STEPS ***"
echo "Running containers in interactive mode with logging"
echo "Please quit with CTRL-C when done viewing output"
echo "*** VERIFY NO ERRORS ***"
sleep 5.0

if [ "${USER_OS}" == "Windows" ];then
  docker-compose -f ./../docker-compose-win.yml up --build
else
  docker-compose up --build
fi

sleep 2.0
echo "***Vi starter lige forfra***"
docker-compose down

echo "*** RE-STARTING SERVICES AND BROWSER ***"
docker-compose up -d
sleep 2.0
if [ "${USER_OS}" == "Windows" ];then
  start firefox $URL_WIN:$PORT
  echo "***Starting firefox***"
elif [ "${USER_OS}" == "macOS" ];then
  open "${URL}:${PORT}"
elif [ "${USER_OS}" == "Linux" ];then
  xdg-open "${URL}:${PORT}"
else
  echo "${USER_OS} OS, Please manually open browser on: ${URL}:${PORT}"
fi
