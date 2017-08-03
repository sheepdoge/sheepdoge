#!/bin/bash
#
# Provision the docker container with sheepdog.

DIR=/test/kennels/kennel-update-kennel-before-cron-sample

cd $DIR;\
sheepdog install &&\
sheepdog run --run-mode bootstrap &&\
sheepdog run &&\
echo 'Waiting 120 seconds for cron job to execute' &&\
sleep 120
