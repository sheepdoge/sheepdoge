#!/bin/bash
#
# Provision the docker container with sheepdoge.

DIR=/test/kennels/kennel-cron-bootstrap-sample

cd $DIR;\
sheepdoge install &&\
sheepdoge run --run-mode bootstrap &&\
sheepdoge run
