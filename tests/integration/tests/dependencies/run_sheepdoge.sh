#!/bin/bash
#
# Provision the docker container with sheepdoge.

DIR=/test/kennels/kennel-dependencies

cd $DIR; ../../sheepdoge_runner.py install && ../../sheepdoge_runner.py run --run-mode bootstrap
