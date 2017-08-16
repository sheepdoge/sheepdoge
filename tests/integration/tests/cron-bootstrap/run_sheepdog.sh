#!/bin/bash
#
# Provision the docker container with sheepdog.

DIR=/test/kennels/kennel-cron-bootstrap-sample

cd $DIR;\
sheepdog install &&\
sheepdog run --run-mode bootstrap &&\
sheepdog run
