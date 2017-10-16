#!/bin/bash

set -e

IMAGE_NAME=sheepdoge/test_dependencies
DIR=/test

# Move the necessary files within the parent directory to this directory so that
# we can access them in the Dockerfile.
SD=$(dirname $0)
TMP_SCRATCH="$SD/tmp_scratch"
mkdir $TMP_SCRATCH

teardown() {
    rm -r $TMP_SCRATCH
}

trap 'teardown' EXIT

mkdir "$TMP_SCRATCH/kennels"
cp -r "$SD/../../kennels/kennel-dependencies" "$TMP_SCRATCH/kennels/kennel-dependencies"

mkdir "$TMP_SCRATCH/pups"
cp -r "$SD/../../pups/pup-base" "$TMP_SCRATCH/pups/pup-base"
cp -r "$SD/../../pups/pup-dependencies" "$TMP_SCRATCH/pups/pup-dependencies"
cp "$SD/../../../../sheepdoge_runner.py" "$TMP_SCRATCH/"
cp "$SD/../../../../setup.py" "$TMP_SCRATCH/"
cp -r "$SD/../../../../sheepdoge" "$TMP_SCRATCH/sheepdoge"

docker build -t $IMAGE_NAME .

IS_INTERACTIVE=false

while [ $# -ne 0 ]
do
    case "$1" in
    --interactive)
        IS_INTERACTIVE=true
        ;;
    *)
        ;;
    esac
    shift
done

if [ "$IS_INTERACTIVE" == "true" ]
then
    docker run -it $IMAGE_NAME /bin/bash
else
    docker run $IMAGE_NAME /bin/bash -c "$DIR/run_sheepdoge.sh && $DIR/assert_e2e_state.sh"
fi
