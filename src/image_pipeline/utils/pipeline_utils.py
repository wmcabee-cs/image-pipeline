from image_pipeline.utils.schema_utils import validate_input_fields, validate_output_fields
from image_pipeline.utils.skill_utils import SkillSpec
from typing import Dict, List, Optional, Callable, Sequence, Any
from functools import partial
from toolz import merge
import inspect


def _run_skill(func, input, request):
    params = inspect.signature(func).parameters

    kwargs = {}
    if 'request' in params:
        print(f"\t- request added to input: {request}")
        kwargs['request'] = request
    if 'input' in params:
        print(f"\t- input: {type(input)}")
        kwargs['input'] = input

    output = func(**kwargs)
    print(f"\t- output {type(output)}")
    return output


def run_pipeline(pipeline: List[SkillSpec], request: Dict):
    input = None

    print(f">> request: {request}")

    for skill in pipeline:
        print(f">> running skill {skill}")
        validate_input_fields(skill=skill, input=input)
        output = _run_skill(skill.func, input=input, request=request)
        validate_output_fields(skill=skill, output=output)
        input = output

    print(f">> output: {type(output)}")
    return output


def map_merge(*, func: Callable, reader: Sequence[Dict],
              func_args: Optional[List[str]] = None, func_params: Optional[Dict[str, Any]] = None):
    if func_args is None:
        func_args = []

    get_args = lambda drec: {x: drec[x] for x in func_args}

    if func_params is not None:
        func = partial(func, **func_params)
    reader = (merge(func(**get_args(drec)), drec) for drec in reader)
    return reader
