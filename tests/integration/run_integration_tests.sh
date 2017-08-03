#!/bin/bash
#
# Run all sheepdog integration tests. Sheepdog has a number of different
# integration tests, each one representing a different main feature through an
# example.

set -e

INTERACTIVE_FLAG=

while [ $# -ne 0 ]
do
    case "$1" in
    --interactive)
        INTERACTIVE_FLAG="--interactive"
        ;;
    *)
        ;;
    esac
    shift
done

SD="$(pwd)/$(dirname $0)"

cd $SD/tests/trivial; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
cd $SD/tests/cron-bootstrap; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
cd $SD/tests/dependencies; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
cd $SD/tests/external-pups; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
cd $SD/tests/update-kennel-before-cron; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
