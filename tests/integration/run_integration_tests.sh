#!/bin/bash
#
# Run all sheepdoge integration tests. Sheepdoge has a number of different
# integration tests, each one representing a different main feature through an
# example.
#
# By default, we run all tests in parallel, unless we are in `interactive` mode,
# or set the `sequential` flag.

set -e

INTERACTIVE_FLAG=
SEQUENTIAL=
SD="$(pwd)/$(dirname $0)"

run_integration_tests::sequential() {
    cd $SD/tests/trivial; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
    cd $SD/tests/cron-bootstrap; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
    cd $SD/tests/dependencies; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
    cd $SD/tests/external-pups; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
    cd $SD/tests/update-kennel-before-cron; /bin/bash ./run_test.sh $INTERACTIVE_FLAG;
}

run_integration_tests::parallel() {
    ls -d $SD/tests/* | parallel 'cd {}; /bin/bash ./run_test.sh'
}

while [ $# -ne 0 ]
do
    case "$1" in
    --interactive)
        INTERACTIVE_FLAG="--interactive"
        ;;
    --sequential)
        SEQUENTIAL="true"
        ;;
    *)
        ;;
    esac
    shift
done

if [ ! -z "$INTERACTIVE_FLAG" ] || [ "$SEQUENTIAL" = "true" ]
then
    run_integration_tests::sequential
else
    run_integration_tests::parallel
fi
