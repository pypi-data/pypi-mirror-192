import os
import click

from .config import get_config, Config
from .cli_context import get_context

from .commands.postman import postman_group
from .commands.envs import envs_group
from .commands import config as config_
from .commands import ci


def get_cli(config: Config):
    cli = click.Group(context_settings=get_context(config))
    cli.add_command(postman_group)
    cli.add_command(envs_group)
    cli.add_command(config_.group)
    cli.add_command(ci.command)
    return cli


def init_cli():
    config = get_config()
    init_fs_sturcture(config)
    cli = get_cli(config)
    return cli

def launch_cli():
    cli = init_cli()
    cli()


def init_fs_sturcture(config: Config):
    if not os.path.exists(config.data_folder):
        os.makedirs(config.data_folder)

    if not os.path.exists(config.var_folder):
        os.makedirs(config.var_folder)



