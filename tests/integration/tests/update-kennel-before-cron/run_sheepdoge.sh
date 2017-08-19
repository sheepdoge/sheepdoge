#!/bin/bash
#
# Provision the docker container with sheepdoge.

DIR=/test/kennels/kennel-update-kennel-before-cron-sample

cd $DIR;\
sheepdoge install &&\
sheepdoge run --run-mode bootstrap &&\
sheepdoge run
