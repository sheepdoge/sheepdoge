# pup-trivial-sample

A simple pup for integration testing. It writes an encrypted secret, and
unencrypted variable, and a default value to `~/.pup-trivial-sample-output`.

The integration test asserts correctness by checking the sample file exists with
the proper values.
