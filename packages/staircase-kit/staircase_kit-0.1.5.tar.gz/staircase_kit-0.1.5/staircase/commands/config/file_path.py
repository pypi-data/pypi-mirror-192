import click
import rich

from staircase.config import Config
from staircase.command_providers import config_provider
from staircase.lib.click import async_cmd


@click.command(name="file-path")
@config_provider()
@async_cmd
async def command(config: Config):
    rich.print(config.config_file_path)

