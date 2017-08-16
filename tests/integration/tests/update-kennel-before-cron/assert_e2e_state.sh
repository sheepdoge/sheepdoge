#!/bin/bash

# Note, this script should be run in the docker container.

# Check sheepdog enacted the proper state on the docker container.
# The cron role should have been run 3 times, the no-special-tag role should have
# run 2 times, and the bootstrap role should have run 1 time.

set -e

MAX_TRIES=120

# First argument is file, second is pattern, third is the min number of occurrences
# of pattern we expect in file.
assert_e2e_state::check_occurrences_in_file() {
    tries=0
    success=false

    while [ "$tries" -lt "$MAX_TRIES" ]
    do
        matches=$(grep -s "$2" "$1" | wc -l)

        if [ "$matches" -lt "$3" ]
        then
            sleep 1
            let "tries += 1"
        else
            success=true
            break
        fi
    done

    if [ "$success" = false ]
    then
        echo "Failed $1, $2, $3" >&2
        exit 1
    fi
}

assert_e2e_state::check_occurrences_in_file ~/.pup-cron-output "encrypted_nightly_test" 3
assert_e2e_state::check_occurrences_in_file ~/.pup-no-special-tag-output "unencrypted_var_test" 2
assert_e2e_state::check_occurrences_in_file ~/.pup-bootstrap-output "encrypted_boot_test" 1

exit 0
