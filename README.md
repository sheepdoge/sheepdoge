# sheepdog

Manage your personal Unix machine(s) with [Ansible](https://www.ansible.com/)
(aka [boxen](https://github.com/boxen/boxen) but for ansible).

## Overview

*sheepdog* offers opinionated automated provisioning of your personal Unix
systems.

To use *sheepdog* for your personal configuration, you create your own
*kennel*. The *kennel* describes the overall state you desire for your machine.
For example, you could customize your *kennel*, called `kennel-mattjmcnaughton`,
to install Docker, download the
most recent version of your dotfiles, and upload the public ssh key to Github,
if it isn't there already. Think of a *kennel* like a simple [ansible
playbook](http://docs.ansible.com/ansible/playbooks.html) that conforms to
certain guidelines.

We build a *kennel* by combining *pups*. A *pup* ensures your machine obtains
and maintains a given state. For example, we could create a simple *pup*, called
`pup-sheepdog-configuration`, responsible for ensuring the file `~/.sheepdog.cfg`
exists on your filesystem. If we include `pup-sheepdog-configuration` in our
*kennel*, when we run the *kennel*, *sheepdog* will check whether the
`~/.sheepdog.cfg` file exists, and create it if necessary. Think of a *pup* like
an [ansible role](http://docs.ansible.com/ansible/playbooks_roles.html#roles)
that conforms to certain guidelines.

*sheepdog* is the command line tool which ties everything together, and makes
*kennels* and *pups* not just config files on your machine, but rather powerful
descriptors of your personal systems' state.
