# update-kennel-before-cron

An e2e test asserting our cron job running `sheepdog run --run-mode cron` first
pulls the most recent copy of the kennel from the remote git url and runs
`sheepdog install`.
