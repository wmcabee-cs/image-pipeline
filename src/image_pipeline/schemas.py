from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class RequestParameters:
    path: str
    outfile: str


@dataclass(frozen=True)
class RawImage:
    image_url: str
    # comment: str


@dataclass(frozen=True)
class DominantColor:
    fractionOfPixels: float
    rgbValues: str
    score: float


@dataclass(frozen=True)
class DominantColorList:
    dominant_colors: Optional[List[DominantColor]]


@dataclass(frozen=True)
class BoundingBox:
    boundingPoly: List[int]
    confidence: float
    importanceFraction: float


@dataclass(frozen=True)
class BoundingBoxList:
    bounding_boxes: Optional[List[BoundingBox]]


@dataclass(frozen=True)
class Landmark:
    confidence: float
    landmark: str


@dataclass(frozen=True)
class LandmarkList:
    landmarks: Optional[List[Landmark]]


@dataclass(frozen=True)
class AnnotatedImage(LandmarkList, BoundingBoxList, DominantColorList, RawImage):
    pass
