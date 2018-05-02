#!/bin/bash
#
# Provision the docker container with sheepdoge.

DIR=/test/kennels/kennel-external-pups

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

cd $DIR; ../../sheepdoge.par install && ../../sheepdoge.par run
