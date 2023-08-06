import click

from staircase.config import Config, UserConfig
from staircase.lib.click import async_cmd
from staircase.command_providers import config_provider


@click.command(name="setup")
@click.option("--postman-api-key", prompt="Postman api key")
@click.option("--marketplace-api-key", prompt="Marketplace api key")
@click.option("--github-token", prompt="Github token. With authorized github cli")
@click.option(
    "--ci-env",
    prompt="Default ENV for ci. Ex. `marketplace.staircaseapi.com` this one will be used by default.",
)
@config_provider()
@async_cmd
async def command(config: Config, postman_api_key: str, marketplace_api_key, github_token, **_):
    user_cfg = UserConfig(
        postman_api_key=postman_api_key, marketplace_api_key=marketplace_api_key, github_token=github_token
    )
    config.write_user_cfg(user_cfg=user_cfg)
