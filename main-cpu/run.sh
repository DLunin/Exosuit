#!/bin/bash
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PROJECT_DIR=$SCRIPT_DIR/..
CONTAINER_SCRIPT_DIR=${SCRIPT_DIR/$HOME/\/home/ubuntu}

USER_ID=$(id -u ${USER})
USER_NAME=$(getent group "$(id -g ${USER})" | cut -d: -f1)

COLOR='\u001b[38;5;208;1m'
NO_COLOR='\033[0m'

pushd $SCRIPT_DIR

echo -e "${COLOR}Building the Exosuit main-cpu container${NO_COLOR}"

sudo docker build \
	--build-arg PROJECT_PATH=$PROJECT_DIR \
	. -t exosuit-main-cpu

if [ $? -eq 0 ]; then
    echo -e "${COLOR}Build successful${NO_COLOR}"
else
    echo -e "${COLOR}Build failed${NO_COLOR}"
	exit 1
fi

echo -e "${COLOR}Launching the Exosuit main-cpu container as user '$USER_NAME'${NO_COLOR}"

sudo docker run --rm -it -v $HOME:$HOME \
	-v $PROJECT_DIR:$PROJECT_DIR \
	-w $SCRIPT_DIR/../../ \
	-v "/etc/group:/etc/group:ro" \
	-v "/etc/passwd:/etc/passwd:ro" \
	-v "/etc/shadow:/etc/shadow:ro" \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-u $USER_ID:$USER_ID \
	--net=host \
	 \
	exosuit-main-cpu /bin/bash

popd