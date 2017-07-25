#!/bin/bash
#
# Run all sheepdog integration tests. Sheepdog has a number of different
# integration tests, each one representing a different main feature through an
# example.

set -e

SD="$(pwd)/$(dirname $0)"

cd $SD/tests/trivial; /bin/bash ./run_test.sh;
cd $SD/tests/cron-bootstrap; /bin/bash ./run_test.sh;
