"""The point of entry for the sheepdog pip package console script"""

import click

from sheepdog.app import Sheepdog
from sheepdog.config import Config
from sheepdog.action.install import InstallAction
from sheepdog.action.run import RunAction

ACTIONS = {
    'install': InstallAction,
    'run': RunAction
}

@click.command()
@click.argument('action', type=click.Choice(ACTIONS.keys()))
@click.option('--config-file', default='kennel.cfg')
def cli(action, config_file):
    """CLI for sheepdog interactions.

    :param action: Which cli action we wish to take.
    :type action: str
    :param config_file: Path to kennel configuration. If not specified, use
    `./kennel.cfg`
    :type config_file: str
    """
    with open(config_file, 'r') as config_file_open_for_reading:
        config_file_contents = config_file_open_for_reading.read()

    Config.initialize_config_singleton(config_file_contents)
    action = ACTIONS[action]()

    sheepdog = Sheepdog(action)
    sheepdog.run()

def main():
    """The entry point for running `sheepdog`."""
    # pylint: disable=no-value-for-parameter
    cli()
