# sheepdoge

[![Build
Status](https://travis-ci.org/sheepdoge/sheepdoge.svg?branch=master)](https://travis-ci.org/sheepdoge/sheepdoge)

Manage your personal Unix machine(s) with [Ansible](https://www.ansible.com/)
(aka [boxen](https://github.com/boxen/boxen) but for Ansible).

With *sheepdoge*, provisioning a personal Unix machine can be as easy as:

```bash
$ sheepdoge install && sheepdoge run
```

For more info on how *sheepdoge* works, read on. If you want to get your hands
dirty with *sheepdoge* asap, check out [sheepdoge up and
running](./docs/sheepdoge_up_and_running.md).

## How it works

sheepdoge has three main components:

The *kennel* describes the overall state you desire for your machine.
Think of a *kennel* like a simple [Ansible
playbook](http://docs.ansible.com/ansible/playbooks.html) that conforms to
certain guidelines.

A *pup* ensures your machine obtains
and maintains a given state. Think of a *pup* like
an [Ansible role](http://docs.ansible.com/ansible/playbooks_roles.html#roles)
that conforms to certain guidelines.
Your personal *kennel* can consist not only of *pups* you've created,
but also *pups* created by other *sheepdoge* community members.

*sheepdoge* is the command line tool which ties everything together.

## Features

*sheepdoge* manages the messy corners of using Ansible to manage multiple
personal workstations. It provides the following benefits:

1. **Opinionated design**: *sheepdoge* specifies a number of guidelines for
   *pups* and *kennels*, to ensure everything works together nicely.
2. **Change once, run everywhere**: If you have multiple machines,
   *sheepdoge* prevents configuration drift by regularly running the most recent
   version of your *kennel* on all of your machines.
3. **Get up and going immediately**: Say your hard drive becomes corrupt,
   so you buy a new computer. Run `sheepdoge install && sheepdoge run`,
   and you're new machine is ready to go!
4. **Secret management**: Secret management across multiple machines is a pain.
   It often leads to a lot of copy and paste or manually sending secrets
   unencrypted from machine to machine. *sheepdoge* makes it easy.
5. **Dependency management**: Need a specific python package or ansible role in
   support of your *pup*? *sheepdoge* handles installation.

## Installation

*sheepdoge* depends on `git`, `python`, and `pip`. Install *sheepdoge* by running:

```
pip install sheepdoge
```

## Writing your first kennel

Check out [Creating your first kennel](./docs/creating_your_first_kennel.md) for
step by step instructions on creating your first kennel.

## Writing your first pup

Check out [Creating your first pup](./docs/creating_your_first_pup.md) for step
by step instructions to creating your first pup.

## Contributing

We appreciate and encourage any contributions to *sheepdoge* :dog: Please open an
[issue](https://github.com/sheepdoge/sheepdoge/issues) or [pull
request](https://github.com/sheepdoge/sheepdoge/pulls). It doesn't have to
be a huge feature - documentation fixes/improvements, added test coverage, and
small refactorings for cleaner code are all great places to start :)

*sheepdoge* integration tests depend on Docker. Additionally, if developing on
*sheepdoge*, you'll need to install the development dependencies using [pipenv]
(https://github.com/kennethreitz/pipenv) by running:

```
make install
```

Note, that if you are adding a production dependency to `sheepdoge`, please be
sure to add it both to the `install_requires` section of `setup.py` and
`Pipfile`.

## Support

If you would like to contribute, and would like some help getting started,
please email mattjmcnaughton [@] gmail.com.

## License

*sheepdoge* is licensed under the
[Apache](https://github.com/sheepdoge/sheepdoge/blob/master/LICENSE)
license.
