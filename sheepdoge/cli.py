"""The point of entry for the sheepdoge pip package console script"""

import io

import click

from sheepdoge.action.install import InstallAction, ParallelInstallAction
from sheepdoge.action.run import RunAction
from sheepdoge.app import Sheepdoge
from sheepdoge.config import Config
from sheepdoge.pup import Pup
from sheepdoge.kennel import Kennel


def _initialize_config(config_file, config_options=None):
    config_options = config_options or {}

    with io.open(config_file, 'r',
                 encoding='utf-8') as config_file_open_for_reading:
        config_file_contents = config_file_open_for_reading.read()

    Config.initialize_config_singleton(
        config_file_contents=config_file_contents,
        config_options=config_options
    )


@click.group()
def cli():
    pass


@cli.command()
@click.option('--config-file', default='kennel.cfg')
@click.option('--parallel/--no-parallel', default=True)
def install(config_file, parallel):
    _initialize_config(config_file)

    install_cls = InstallAction

    if parallel:
        install_cls = ParallelInstallAction

    install_action = install_cls(Kennel, Pup)
    Sheepdoge(install_action).run()


@cli.command()
@click.option('--ansible-args', type=str)
@click.option('--config-file', default='kennel.cfg')
def run(ansible_args, config_file):
    _initialize_config(config_file)

    kennel = Kennel(additional_ansible_args=ansible_args)
    run_action = RunAction(kennel)
    Sheepdoge(run_action).run()


def main():
    cli()
