import rich
import os
import json
from pydantic import BaseModel
from pathlib import Path
from typing import Optional


def get_config() -> "Config":
    config = Config()
    try:
        config.load_user_cfg()
    except ConfigNotValidException:
        rich.print("[red]Config is not valid, taking default values.")
    return  config


class UserConfig(BaseModel):
    postman_api_key: Optional[str]
    marketplace_api_key: Optional[str]
    default_ci_env: Optional[str]
    github_token: Optional[str]

STAIRCASE_FOLDER = (Path.home() / '.staircase').absolute()

DATA_FOLDER =  (STAIRCASE_FOLDER / "data").absolute()
VAR_FOLDER = (STAIRCASE_FOLDER / "var").absolute()


class Config:
    var_folder = VAR_FOLDER
    data_folder = DATA_FOLDER

    def __init__(self):
        self.config_file_path = DATA_FOLDER / "config.json"
        self.env_file_path = DATA_FOLDER / "staircase_envs.json"
        self._check_config_file_exists()
        

    def _check_config_file_exists(self):
        self.config_file_path.parent.mkdir(exist_ok=True, parents=True)

    def load_user_cfg(self):
        if not os.path.exists(self.config_file_path):
            return
        
        with open(self.config_file_path, "r") as f:
            try:
                config_file = json.load(f)
                user_config = UserConfig.parse_obj(config_file)
            except json.JSONDecodeError:
                raise ConfigNotValidException("Your config is not valid.")

            self.marketplace_api_key = user_config.marketplace_api_key
            self.postman_api_key = user_config.postman_api_key
            self.github_token = user_config.github_token


    def write_user_cfg(self, user_cfg: UserConfig):
        with open(self.config_file_path, "w+") as f:
            json.dump(user_cfg.dict(), f)

class ConfigNotValidException(Exception):
    ...