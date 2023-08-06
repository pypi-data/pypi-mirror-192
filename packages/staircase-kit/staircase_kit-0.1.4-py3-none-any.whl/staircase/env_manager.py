from typing import Optional
from .env_storage import EnvironmentStorage
from .lib.sdk import StaircaseEnvironment
from .config import Config


class EnvironmentManager:
    config: Config

    def __init__(self, config: Config):
        self.config = config
        self.env_storage = EnvironmentStorage(config)

    def get_staircase_env(self, domain: str) -> Optional[StaircaseEnvironment]:
        envs = self.env_storage.get_all_envs()
        if not envs:
            return
        envs = list(filter(lambda e: e.domain_name == domain, envs))
        if not envs:
            return
        env = envs[0]
        return StaircaseEnvironment(domain=env.domain_name, api_key=env.api_key)
