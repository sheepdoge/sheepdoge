# sheepdog

[![Build
Status](https://travis-ci.org/mattjmcnaughton/sheepdog.svg?branch=master)](https://travis-ci.org/mattjmcnaughton/sheepdog)

Manage your personal Unix machine(s) with [Ansible](https://www.ansible.com/)
(aka [boxen](https://github.com/boxen/boxen) but for Ansible).

## Overview

*sheepdog* offers opinionated automated provisioning of your personal Unix
systems.

To use *sheepdog* for your personal configuration, you create your own
*kennel*. The *kennel* describes the overall state you desire for your machine.
For example, you could customize your *kennel*, called `kennel-mattjmcnaughton`,
to install Docker, download the
most recent version of your dotfiles, and upload the public ssh key to Github,
if it isn't there already. Think of a *kennel* like a simple [Ansible
playbook](http://docs.ansible.com/ansible/playbooks.html) that conforms to
certain guidelines.

We build a *kennel* by combining *pups*. A *pup* ensures your machine obtains
and maintains a given state. For example, we could create a simple *pup*, called
`pup-sheepdog-configuration`, responsible for ensuring the file `~/.sheepdog.cfg`
exists on your filesystem. If we include `pup-sheepdog-configuration` in our
*kennel*, when we run the *kennel*, *sheepdog* will check whether the
`~/.sheepdog.cfg` file exists, and create it if necessary. Think of a *pup* like
an [Ansible role](http://docs.ansible.com/ansible/playbooks_roles.html#roles)
that conforms to certain guidelines.

*sheepdog* is the command line tool which ties everything together, and makes
*kennels* and *pups* not just config files on your machine, but rather powerful
descriptors of your personal systems' state.

## Why not just use Ansible?

Sheepdog takes care of the hardest parts of using Ansible to manage your
personal machines. You can focus on specifying the desired state for your
system, and let *sheepdog* take care of the rest. *sheepdog* provides four major
benefits.

1. **Opinionated design**: *sheepdog* specifies a number of guidelines for
   *pups* and *kennels*. We've considered the best practices for managing your
   local system with Ansible, so you don't have to worry about it.
2. **Change once, run everywhere... right away**: *sheepdog* prevents
   configuration drift by regularly running the most recent version of your
   kennel. Say you realize you need to update your version of the `git-all`
   apt-package. Just add it to your *kennel*. If you're using the same
   *kennel* on your home computer, *sheepdog's* will update `git` during its
   regularly scheduled run. No manual steps required.
3. **Batteries included**: *sheepdog* is powerful right out of the box. Say
   you've already created a *kennel*, and you get a new computer. Run `pip
   install sheepdog`, `git clone PATH/TO/kennel-MYUSERNAME.git && cd
   kennel-MYUSERNAME`, and `sheepdog install && sheepdog run`. You're new
   machine is ready to go!
4. **Secret management**: Secret management across multiple machines is a pain.
   It often leads to a lot of copy and paste or manually sending secrets
   unencrypted from machine to machine. But *sheepdog* makes it easy,
   while not sacrificing security.

That being said, if you consider yourself a seasoned Ansible veteran, or don't
like the looks of some of the opinionated design guidelines, then you may prefer
managing your own Ansible setup.

## Getting started

### Install Sheepdog

We recommend installing *sheepdog* through pip.

```
pip install sheepdog
```

### Create a *kennel*

@TODO(mattjmcnaughton)

### Create a *pup*

@TODO(mattjmcnaughton)

## Contributing

@TODO(mattjmcnaughton)

## License

[Apache](https://github.com/mattjmcnaughton/sheepdog/blob/master/LICENSE)
