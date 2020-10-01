#!/usr/bin/env bash

SRC=$(dirname $0)/
DEST=/home/ubuntu/projects/tomato-tracker-flask/

rsync -av -progress --delete -e  "ssh -i ~/.ssh/MyKeyPair.pem" --exclude-from=.rsyncignore \
 ${SRC} ubuntu@$EC2IP4:${DEST}

 ssh -i ~/.ssh/MyKeyPair.pem ubuntu@$EC2IP4 "cd ${DEST} && docker-compose up -d --build && docker ps"