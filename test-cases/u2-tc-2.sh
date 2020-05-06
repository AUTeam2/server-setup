echo "Running testcase: U2.TC-2"
echo "Verifikation af at Django på Docker fungerer på lokalmaskine"
echo "Linux og Mac"

URL=http://auteam2.mooo.com
PORT=8001

SSH_DOMAIN=auteam2.mooo.com
SSH_USERNAME=team2
SSH_PORT=22

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

echo "*** SSH'ing INTO THE SERVER ***"
ssh -p $SSH_PORT -t ${SSH_USERNAME}@${SSH_DOMAIN} "
cd e3pro3/server-setup
pwd
docker ps
sleep 2.0
docker-compose down
docker volume rm data-volume
docker volume rm mqtt-volume
docker volume create data-volume
docker volume create mqtt-volume
git checkout master && git pull
echo '*** TEST STEPS ***' && sleep 5.0
docker-compose up --build && docker-compose down
echo '*** RE-STARTING SERVICES AND LEAVING SSH SERVER ***'
docker-compose up -d
sleep 2.0
exit"

echo "*** OPENING BROWSER ***"
sleep 2.0
if [ "${USER_OS}" == "Windows" ];then
  start firefox $URL_WIN:$PORT
elif [ "${USER_OS}" == "macOS" ];then
  open "${URL}:${PORT}"
elif [ "${USER_OS}" == "Linux" ];then
  xdg-open "${URL}:${PORT}"
else
  echo "${USER_OS} OS, Please manually open browser on: ${URL}:${PORT}"
fi
