"""The point of entry for the sheepdog pip package console script"""

import click

from sheepdog.app import Sheepdog
from sheepdog.config import Config
from sheepdog.action import InstallAction, RunAction

ACTIONS = {
    'install': InstallAction,
    'run': RunAction
}

@click.command()
@click.argument('action', type=click.Choice(ACTIONS.keys()))
@click.option('--config-file')
def cli(action, config_file):
    """CLI for sheepdog interactions.

    :param action: Which cli action we wish to take.
    :type action: str
    :param config_file: Path to `sheepdog.cfg`. If not specified, use
    `./kennel.cfg`
    :type config_file: str
    """
    config = Config(config_file)
    action = ACTIONS[action](config)

    sheepdog = Sheepdog(action)
    sheepdog.run()

def main():
    """The entry point for running `sheepdog`."""
    # pylint: disable=no-value-for-parameter
    cli()
