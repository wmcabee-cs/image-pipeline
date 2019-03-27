from dataclasses import dataclass
from typing import List, Any, Optional, Iterable, Sequence


###################################################
# Input Output Schema
###################################################
@dataclass
class ColorRGB:
    red: int
    green: int
    blue: int


@dataclass
class DataPoint:
    x: int
    y: int


BoundingBox = List[DataPoint]

