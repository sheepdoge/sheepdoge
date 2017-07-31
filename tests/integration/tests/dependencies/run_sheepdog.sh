#!/bin/bash
#
# Provision the docker container with sheepdog.

DIR=/test/kennels/kennel-dependencies

cd $DIR; ../../sheepdog_runner.py install && ../../sheepdog_runner.py run --run-mode bootstrap
