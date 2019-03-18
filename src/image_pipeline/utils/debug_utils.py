import sys
import json
from pathlib import Path
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass
from importlib import import_module

DEFAULT_CONFIG_F = Path('~/.cortex/config').expanduser()


class StopEarlyException(Exception):
    pass


def runit(func: Callable, **kwargs):
    try:
        ret = func(**kwargs)
        return ret
    except StopEarlyException as e:
        return e.args


def retval(args: Any):
    raise StopEarlyException(args)


############################

def get_cortex_config(config_f: Path = DEFAULT_CONFIG_F):
    config = json.load(config_f.open())
    return config


def get_cortex_profile(name: Optional[str], config=None):
    if config is None:
        config = get_cortex_config()

    if name is None:
        name = config['currentProfile']

    try:
        return config['profiles'][name]
    except KeyError as e:
        print(f"error: problem access profile {name}. Try {sorted(config['profiles'])}")
        raise


def call_cortex_function(func: Callable, payload: Dict, profile_name: Optional[str] = None):
    # load info from the cortex configuration
    profile = get_cortex_profile(name=profile_name)

    params = {
        "activationId": "",
        "instanceId": 1,
        "sessionId": 1,
        "timestamp": 1,
        "channelId": 1,
        "token": profile['token'],
        "apiEndpoint": profile['url'],
        "payload": payload,
        "properties": {},
        "datasetBindings": [],
        "entityBindings": [],
        "typeName": "",
        "tenantId": ""
    }

    return func(params)


@dataclass
class prepend_syspath:
    path: str

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass



SKILLS_D = Path('/Users/wmcabee/PycharmProjects/image_pipeline/skills')


def load_skill_module(skill_name):
    skill_d = SKILLS_D / skill_name / 'src'

    with prepend_syspath(path=str(skill_d)):
        skill_path = f"{skill_name}.__main__"
        module = import_module(skill_path)
    return module
