# cron-bootstrap

An e2e test checking that the cron/bootstrap functionality works as expected.
Namely, we only run pups with the bootstrap label when in `bootstrap` run mode,
and `pup-base` successfully creates a cron job to run pups with the `cron` label
at the user specified interval.
