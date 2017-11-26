#!/bin/bash

# Note, this script should be run in the docker container.

# Check sheepdoge enacted the proper state on the docker container.
# In this context, checking that the proper secrets were written to a file.
# Look at kennel-trivial-sample/vars/*.yml to determine the variable values.

set -e

OUTPUT_FILE=~/.pup-trivial-sample-output

grep -s encrypted_nightly_test $OUTPUT_FILE
grep -s encrypted_boot_test $OUTPUT_FILE
grep -s unencrypted_var_test $OUTPUT_FILE
