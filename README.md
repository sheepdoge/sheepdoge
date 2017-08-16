# sheepdog

[![Build
Status](https://travis-ci.org/mattjmcnaughton/sheepdog.svg?branch=master)](https://travis-ci.org/mattjmcnaughton/sheepdog)

Manage your personal Unix machine(s) with [Ansible](https://www.ansible.com/)
(aka [boxen](https://github.com/boxen/boxen) but for Ansible).

With *sheepdog*, provisioning a personal Unix machine can be as easy as:

```bash
$ sheepdog install && sheepdog run --bootstrap
```

## How it works

Sheepdog has three main components:

The *kennel* describes the overall state you desire for your machine.
Think of a *kennel* like a simple [Ansible
playbook](http://docs.ansible.com/ansible/playbooks.html) that conforms to
certain guidelines.

A *pup* ensures your machine obtains
and maintains a given state. Think of a *pup* like
an [Ansible role](http://docs.ansible.com/ansible/playbooks_roles.html#roles)
that conforms to certain guidelines.
Your personal *kennel* can consist not only of *pups* you've created,
but also *pups* created by other *sheepdog* community members.

*sheepdog* is the command line tool which ties everything together.

## Features

*sheepdog* manages the messy corners of using Ansible to manage multiple
personal workstations. It provides the following benefits:

1. **Opinionated design**: *sheepdog* specifies a number of guidelines for
   *pups* and *kennels*, to ensure everything works together nicely.
2. **Change once, run everywhere**: If you have multiple machines,
   *sheepdog* prevents configuration drift by regularly running the most recent
   version of your *kennel* on all of your machines.
3. **Get up and going immediately**: Say your hard drive becomes corrupt,
   so you buy a new computer. Run `sheepdog install && sheepdog run --bootstrap`,
   and you're new machine is ready to go!
4. **Secret management**: Secret management across multiple machines is a pain.
   It often leads to a lot of copy and paste or manually sending secrets
   unencrypted from machine to machine. *sheepdog* makes it easy.
5. **Dependency management**: Need a specific python package or ansible role in
   support of your *pup*? *sheepdog* handles installation.

## Installation

*sheepdog* depends on `git`, `python`, and `pip`. Install *sheepdog* by running:

```
pip install sheepdog
```

## Writing your first kennel

@TODO(mattjmcnaughton)

## Writing your first pup

@TODO(mattjmcnaughton)

## Contributing

We appreciate and encourage any contributions to *sheepdog* :dog: Please open an
[issue](https://github.com/mattjmcnaughton/sheepdog/issues) or [pull
request](https://github.com/mattjmcnaughton/sheepdog/pulls). It doesn't have to
be a huge feature - documentation fixes/improvements, added test coverage, and
small refactorings for cleaner code are all great places to start :)

*sheepdog* integration tests depend on Docker. Additionally, if developing on
*sheepdog*, you'll need to install the development dependencies by running:

```
pip install -r requirements.txt
python setup.py develop
```

## Support

If you would like to contribute, and would like some help getting started,
please email mattjmcnaughton [@] gmail.com.

## License

*sheepdog* is licensed under the
[Apache](https://github.com/mattjmcnaughton/sheepdog/blob/master/LICENSE)
license.
