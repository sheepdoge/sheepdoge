#!/bin/bash
#
# Provision the docker container with sheepdog.

DIR=/test

# @TODO(mattjmcnaughton) This should run `sheepdog install` and `sheepdog run`
# with the proper kennel file.
cd $DIR; ./sheepdog_runner.py
