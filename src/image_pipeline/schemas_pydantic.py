from pydantic import BaseModel, UrlStr
from typing import List, Optional


class ImmutableBaseModel(BaseModel):
    class Config:
        allow_mutation = False


class RequestParameters(ImmutableBaseModel):
    path: str
    outfile: str


class RawImage(ImmutableBaseModel):
    image_url: UrlStr
    comment: Optional[str]


class DominantColor(ImmutableBaseModel):
    fractionOfPixels: float
    rgbValues: str
    score: float


class DominantColorList(ImmutableBaseModel):
    dominant_colors: Optional[List[DominantColor]]


class BoundingBox(ImmutableBaseModel):
    boundingPoly: List[int]
    confidence: float
    importanceFraction: float


class BoundingBoxList(ImmutableBaseModel):
    bounding_boxes: Optional[List[BoundingBox]]


class Landmark(ImmutableBaseModel):
    confidence: float
    landmark: str


class LandmarkList(ImmutableBaseModel):
    landmarks: Optional[List[Landmark]]


class AnnotatedImage(LandmarkList, BoundingBoxList, DominantColorList, RawImage):
    pass
