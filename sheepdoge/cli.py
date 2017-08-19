"""The point of entry for the sheepdoge pip package console script"""

import click

from sheepdoge.action.install import InstallAction
from sheepdoge.action.run import RunAction
from sheepdoge.app import Sheepdoge
from sheepdoge.config import Config, KennelRunModes


def _initialize_config(config_file, config_options=None):
    config_options = config_options or {}

    with open(config_file, 'r') as config_file_open_for_reading:
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
def install(config_file):
    _initialize_config(config_file)

    install_action = InstallAction()
    Sheepdoge(install_action).run()


@cli.command()
@click.option('--run-mode', default=KennelRunModes.NORMAL,
              type=click.Choice([KennelRunModes.NORMAL,
                                 KennelRunModes.BOOTSTRAP,
                                 KennelRunModes.CRON]))
@click.option('--config-file', default='kennel.cfg')
def run(run_mode, config_file):
    config_options = {
        'kennel_run_mode': run_mode
    }

    _initialize_config(config_file, config_options)

    run_action = RunAction()
    Sheepdoge(run_action).run()


def main():
    cli()
