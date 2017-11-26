#!/bin/bash
#
# Provision the docker container with sheepdoge.

DIR=/test/kennels/kennel-update-kennel-before-cron-sample

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

cat <<EOT >> ~/.bashrc
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
EOT

cd $DIR;\
sheepdoge install &&\
sheepdoge run --run-mode bootstrap &&\
sheepdoge run
