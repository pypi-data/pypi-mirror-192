from envparse import Env

env = Env(
    APP_NAME=str,
    LOG_LEVEL=str,
    HOST=str,
    PORT=str,
    RELOAD=str,
    DB_HOST=str,
    DB_PORT=str,
    DB_USER=str,
    DB_PASS=str,
    DB_DATABASE=str,
)
env.read_envfile()


def load(config):
    print("Config: ", config)
    if env is not None:
        return env.str(config)
    else:
        raise Exception("Config ", config, " not found")
