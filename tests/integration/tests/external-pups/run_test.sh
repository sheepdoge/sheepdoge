#!/bin/bash

set -e

IMAGE_NAME=sheepdog/test_external_pups
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
cp -r "$SD/../../kennels/kennel-external-pups" "$TMP_SCRATCH/kennels/kennel-external-pups"

mkdir "$TMP_SCRATCH/pups"
cp -r "$SD/../../pups/pup-base" "$TMP_SCRATCH/pups/pup-base"
cp "$SD/../../../../sheepdog_runner.py" "$TMP_SCRATCH/"
cp "$SD/../../../../requirements.txt" "$TMP_SCRATCH/"
cp "$SD/../../../../setup.py" "$TMP_SCRATCH/"
cp -r "$SD/../../../../sheepdog" "$TMP_SCRATCH/sheepdog"

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
    docker run $IMAGE_NAME /bin/bash -c "$DIR/run_sheepdog.sh && $DIR/assert_e2e_state.sh"
fi
