"""The point of entry for the sheepdog pip package console script"""

import click

from sheepdog.action.install import InstallAction
from sheepdog.action.run import RunAction
from sheepdog.app import Sheepdog
from sheepdog.config import Config, KennelRunModes
from sheepdog.exception import SheepdogCLIImproperArgumentsException

ACTIONS = {
    'install': InstallAction,
    'run': RunAction
}

@click.command()
@click.argument('action', type=click.Choice(ACTIONS.keys()))
@click.option('--config-file', default='kennel.cfg')
@click.option('--run-mode', type=click.Choice([KennelRunModes.NORMAL,
                                               KennelRunModes.BOOTSTRAP,
                                               KennelRunModes.CRON]))
def cli(action, config_file, run_mode):
    """CLI for sheepdog interactions.

    :param action: Which cli action we wish to take.
    :type action: str
    :param config_file: Path to kennel configuration. If not specified, use
    `./kennel.cfg`
    :type config_file: str
    :param run_mode: The mode in which `sheepdog run` is occurring (i.e.
    cron, bootstrap...`
    :type run_mode: str
    """
    with open(config_file, 'r') as config_file_open_for_reading:
        config_file_contents = config_file_open_for_reading.read()

    config_options = {}

    if run_mode is not None:
        if action != 'run':
            err_msg = 'Cannot specify `run_mode` if action is not `run`.'
            raise SheepdogCLIImproperArgumentsException(err_msg)

        config_options['kennel_run_mode'] = run_mode

    Config.initialize_config_singleton(
        config_file_contents=config_file_contents,
        config_options=config_options
    )

    action = ACTIONS[action]()

    sheepdog = Sheepdog(action)
    sheepdog.run()


def main():
    """The entry point for running `sheepdog`."""
    # pylint: disable=no-value-for-parameter
    cli()
