#!/usr/bin/env bash

# Define test cases for videostream
# TC-1: Der vises en test stream af en vimpel på vstream/test-stand/0
# TC-2: Kan "installere" et webcam og vise det på den tilhørende html side 
# TC-3: Kan "afinstallere" et webcam og vise standard besked hvis html tilgås

URL=http://127.0.0.1
PORT=5555
start=0

#Font colours
RED='\033[1;31m'         # Bold red
GREEN='\033[0;32m'       # Bold green
YELLOW='\033[0;33m'      # Bold yellow
HEAD='\033[1;37;44m'
NC='\033[0m'             # No Color

countdown(){
    if (( $seconds % 10 == 0 ));then
        echo -e ""${YELLOW}"Time until next test: ${seconds} seconds"${NC}""
        echo ""

    elif [[ $seconds -eq 3 ]];then
        echo ""
        echo "   xxx   "
        echo " xxxxxx  "
        echo "xxx  xx "
        echo "    xxx  "
        echo "xxx  xx  "
        echo " xxxxxx  "
        echo "   xxx   "
        echo ""

    elif [[ $seconds -eq 2 ]];then
        echo "   xxx   "
        echo " xxxxxx  "
        echo "xxx  xxx "
        echo "   xxx   "
        echo " xxx     "
        echo " xxxxxxx "
        echo ""

    elif [[ $seconds -eq 1 ]];then
        echo "   xxx    "
        echo "  xxxx    "
        echo " xxxxx    "
        echo "   xxx    "
        echo "   xxx    "
        echo " xxxxxxx  "
        echo ""

    else
        continue
        # echo "${pattern}"
    fi
}

# Vid_TC-1-A
echo -e ""${HEAD}"Vid_TC-1-A to Test video in API point on /0"${NC}""
TC1MSG="Er der vist en stream af en vimpel?', (enter: yes/no)"
echo "Enter go"
read starttest

if [ "${starttest}" == "go" ]; then
    seconds=3
    while [ $seconds -gt 0 ]
    do       
        countdown
        sleep 1s
        seconds=$(( $seconds - 1 ))

    done # Time Delay (Seconds) 
    start chrome ${URL}:${PORT}/vstream/test-stand/0
    sleep 2.0
    echo -e ""${YELLOW}${TC1MSG}${NC}""
    result=" "
    quit=0
    until [ "${quit}" ==  1 ] 
    do
        read result
        # Returned test result (PASS/FAIL):
        if [ "${result}" == "no" ]; then
            echo -e "Test${RED} FAILED ${NC}"
            echo " "
            quit=1
            exit -1
        elif [ "${result}" == "yes" ]; then
            echo -e "Test${GREEN} PASSED ${NC}"
            echo " "
            quit=1
        else
            echo "ugyldigt svar"
            echo -e ""${YELLOW}${TC1MSG}${NC}""
        fi
    done
fi


# Vid_TC-2-A
echo -e ""${HEAD}"Vid_TC-2-A to Test video in API point on /67 (Setup Video)"${NC}""
TC2MSG="Er der vist en stream af en vimpel?', (enter: yes/no)"
echo "Enter go"
read starttest

if [ "${starttest}" == "go" ]; then
    curl ${URL}:${PORT}/install-test-stand/67 -d "data="http://188.178.124.160:80/mjpg/video.mjpg"" -X put
    seconds=3
    while [ $seconds -gt 0 ]
    do       
        countdown
        sleep 1s
        seconds=$(( $seconds - 1 ))

    done # Time Delay (Seconds) 
    start chrome ${URL}:${PORT}/vstream/test-stand/67
    sleep 2.0
    echo -e ""${YELLOW}${TC1MSG}${NC}""
    quit=0
    until [ "${quit}" ==  1 ] 
    do
        read result
        # Returned test result (PASS/FAIL):
        if [ "${result}" == "no" ]; then
            echo -e "Test${RED} FAILED ${NC}"
            echo " "
            quit=1
            exit -1
        elif [ "${result}" == "yes" ]; then
            echo -e "Test${GREEN} PASSED ${NC}"
            echo " "
            quit=1
        else
            echo "ugyldigt svar"
            echo -e ""${YELLOW}${TC1MSG}${NC}""
        fi
    done
fi


# Vid_TC-3-A
echo -e ""${HEAD}"Vid_TC-3-A to Test video in API point on /67 (Tear down)"${NC}""
TC3AMSG="Er det vist et billede med 'Prøvestand endnu ikke installeret?', (enter: yes/no)"
echo "Enter go"
read starttest

if [ "${starttest}" == "go" ]; then
    curl ${URL}:${PORT}/install-test-stand/67 -d "data=""" -X put
    seconds=3
    while [ $seconds -gt 0 ]
    do       
        countdown
        sleep 1s
        seconds=$(( $seconds - 1 ))

    done # Time Delay (Seconds) 
    start chrome ${URL}:${PORT}/vstream/test-stand/67
    sleep 2.0
    echo -e ""${YELLOW}${TC3AMSG}${NC}""
    result=" "
    quit=0
    until [ "${quit}" ==  1 ] 
    do
        read result
        # Returned test result (PASS/FAIL):
        if [ "${result}" == "no" ]; then
            echo -e "Test${RED} FAILED ${NC}"
            echo " "
            quit=1
            exit -1
        elif [ "${result}" == "yes" ]; then
            echo -e "Test${GREEN} PASSED ${NC}"
            echo " "
            quit=1
        else
            echo "ugyldigt svar"
            echo -e ""${YELLOW}"Er det vist et billede med 'Prøvestand endnu ikke installeret?', (enter: yes/no)"${NC}""
        fi
    done
fi

# All Tests PASSED:
exit 0