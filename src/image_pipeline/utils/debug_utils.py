import sys
import json
from pathlib import Path
from typing import Dict, Optional, Callable, Any, Mapping
import importlib
import importlib.util
from toolz import merge

DEFAULT_CONFIG_F = Path('~/.cortex/config').expanduser()


class StopEarlyException(Exception):
    pass


def runit(func: Callable, **kwargs):
    try:
        ret = func(**kwargs)
        return ret
    except StopEarlyException as e:
        return e.args
    except Exception as e:
        print('Exception:', e)
        raise


def retval(*args: Any):
    raise StopEarlyException(*args)


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


def call_cortex_function(afunc: Callable,
                         payload: Mapping[str, Any],
                         profile_name: Optional[str] = None,
                         params: Mapping[str, Any] = None,
                         properties: Mapping[str, Any] = None) -> Any:
    if properties is None:
        properties = {}

    profile = get_cortex_profile(name=profile_name)

    merged_params = {
        "activationId": "",
        "instanceId": 1,
        "sessionId": 1,
        "timestamp": 1,
        "channelId": 1,
        "token": profile['token'],
        "apiEndpoint": profile['url'],
        "payload": payload,
        "properties": properties,
        "datasetBindings": [],
        "entityBindings": [],
        "typeName": "",
        "tenantId": ""
    }
    if params is not None:
        merged_params = merge(merged_params, params)

    try:
        return afunc(params=merged_params)
    except StopEarlyException as e:
        print('stopped early ...')
        return e.args


def load_cortex_action(actions_d, action_name):
    file_path = actions_d / action_name / 'src' / '__main__.py'
    spec = importlib.util.spec_from_file_location(action_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[action_name] = module

    return module


''' 
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

def load_skill_module(skills_d, name):
    skill_d = skills_d / name
    print("looking for module in %s" % skill_d)

    with prepend_syspath(path=str(skill_d)):
        skill_path = f"src.__main__"
        old_module =  sys.modules.get(skill_path)
        if old_module is not None:
            module = reload(old_module)
        else:
            module = import_module(skill_path)
    return module
'''
