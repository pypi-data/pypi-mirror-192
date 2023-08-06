import click
import functools as ft

from .cli_context import CONTEXT_CONFIG_KEY

from .postman import PostmanClient, Postman
from .staircase import Staircase
from .env_storage import EnvironmentStorage
from .env_manager import EnvironmentManager
from .config import Config


def postman_provider():
    def decorator(f):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            config: Config = ctx.obj[CONTEXT_CONFIG_KEY]
            postman_client = PostmanClient(api_key=config.postman_api_key)
            postman = Postman(postman_client)
            return ctx.invoke(
                f, *args, **kwargs, postman_client=postman_client, postman=postman
            )

        return ft.update_wrapper(wrapper, f)

    return decorator


def config_provider():
    def decorator(f):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            config: Config = ctx.obj[CONTEXT_CONFIG_KEY]
            return ctx.invoke(f, *args, **kwargs, config=config)

        return ft.update_wrapper(wrapper, f)

    return decorator


def staircase_provider():
    def decorator(f):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            config: Config = ctx.obj[CONTEXT_CONFIG_KEY]
            staircase = Staircase(config)
            return ctx.invoke(f, *args, **kwargs, staircase=staircase)

        return ft.update_wrapper(wrapper, f)

    return decorator


def env_storage_provider():
    def decorator(f):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            config: Config = ctx.obj[CONTEXT_CONFIG_KEY]
            env_storage = EnvironmentStorage(config)
            return ctx.invoke(f, *args, **kwargs, env_storage=env_storage)

        return ft.update_wrapper(wrapper, f)

    return decorator

def env_manager_provider():
    def decorator(f):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            config: Config = ctx.obj[CONTEXT_CONFIG_KEY]
            obj = EnvironmentManager(config)
            return ctx.invoke(f, *args, **kwargs, env_manager=obj)

        return ft.update_wrapper(wrapper, f)

    return decorator

