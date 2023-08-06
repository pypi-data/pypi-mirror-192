from .config import Config

CONTEXT_CONFIG_KEY = 'context'

def get_context(config: Config):
    return {"obj": {CONTEXT_CONFIG_KEY: config}}