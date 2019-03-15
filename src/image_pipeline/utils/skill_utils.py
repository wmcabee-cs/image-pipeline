from dataclasses import dataclass, field
from typing import Callable, FrozenSet, Optional
import pandas as pd
import functools


@dataclass(frozen=True)
class SkillSpec:
    name: str
    func: Callable[[pd.DataFrame], pd.DataFrame] = field(repr=False)
    required_inputs: Optional[FrozenSet[str]]
    add_fields: Optional[FrozenSet[str]] = None

    def __str__(self):
        return f"SkillSpec('{self.name}')"


def build_skill(*, func: Callable, required_inputs=None, add_fields=None, name=None, **kwargs):
    if name is None:
        name = func.__name__

    if len(kwargs) > 0:
        func = functools.partial(func, **kwargs)
    return SkillSpec(name=name, func=func, required_inputs=required_inputs, add_fields=add_fields)
