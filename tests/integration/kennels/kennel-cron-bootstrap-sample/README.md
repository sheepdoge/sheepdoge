# kennel-cron-bootstrap-sample

The kennel testing the functionality which allows us to mark pups as cron,
bootstrap, or neither. `bootstrap` pups are only run when you suffix the `kennel
run` command with `--bootstrap`. We run `cron` pups during any invocation of
`kennel run`, in addition to using `pup-base` to set up a regularly scheduled
cron job to run just the `cron` pups. Finally, we execute pups with no label for
every playbook run, except for the `--cron` run.
