__all__=(
    "get_config_path",
)

import os 
from . import env_args

# get_config_path("redis-conf.json")
def get_config_path(subpath:str):
    return _file_path_join(env_args.CONFIG_ROOT_PATH,subpath)


def _file_path_join(pre,post):
    if not post:
        return pre 
    if post[0]=="/":
        return os.path.join(pre,post[1:])
    return os.path.join(pre,post)