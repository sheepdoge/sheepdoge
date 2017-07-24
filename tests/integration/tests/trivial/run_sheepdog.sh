#!/bin/bash
#
# Provision the docker container with sheepdog.

DIR=/test/kennels/kennel-trivial-sample

cd $DIR; ../../sheepdog_runner.py install && ../../sheepdog_runner.py run --run-mode bootstrap
