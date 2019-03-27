from toolz import get_in, take
from .google_api_utils import post_google_vision_endpoint

# schema imports
from .schema import dataclass
from .schema import List, Optional, Any
from .schema import ColorRGB, BoundingBox, Iterable, Sequence


#######################################
# Helper functions
#######################################

def _add_zeros(point):
    point['x'] = point.get('x', 0)
    point['y'] = point.get('y', 0)
    return point


##############################################
# IDENTIFY COLORS
##############################################
@dataclass
class DominantColorEstimate:
    color: ColorRGB
    score: float
    pixel_fraction: float


@dataclass
class DominantColorAnnotation:
    colors: List[DominantColorEstimate]


def ident_dominant_colors(*, image_url: str, limit: Optional[int]) -> DominantColorAnnotation:
    # Create payload
    payload = {"requests": [
        {"image": {"source": {"imageUri": image_url}}, "features": [{"type": "IMAGE_PROPERTIES"}]},
    ]}

    # Post request
    data = post_google_vision_endpoint(payload=payload)

    # Transform to color output item
    colors = get_in(['responses', 0, 'imagePropertiesAnnotation', 'dominantColors', 'colors'], data)
    colors = sorted(colors, key=lambda x: x['score'], reverse=True)
    if limit is not None:
        colors = list(take(limit, colors))
    colors = list(colors)

    # Return output
    output = {'colors': colors}
    return output


##############################################
# IDENTIFY CROP HINTS
##############################################

@dataclass
class CropHintAnnotation:
    bounding_boxes: List[BoundingBox]
    confidence: float
    importance_fraction: float


def ident_crop_hints(*, image_url: str, aspect_ratios: Optional[float] = 1.0) -> CropHintAnnotation:
    if aspect_ratios is not None:
        aspect_ratios = [aspect_ratios]
    payload = {"requests": [
        {"image": {"source": {"imageUri": image_url}}, "features": [{"type": "CROP_HINTS"}],
         'imageContext': {'cropHintsParams': {'aspectRatios': [aspect_ratios]}},
         },
    ]}
    response = post_google_vision_endpoint(payload=payload)
    hint = get_in(['responses', 0, 'cropHintsAnnotation', 'cropHints', 0], response)

    #########################
    # build boundingBox item
    #  - promote 'vertices' item to top level object
    #  - google api does not return x, y values when zero. Add zeros to vertices pairs where missing
    vertices = get_in(['boundingPoly', 'vertices'], hint)
    bounding_poly = [_add_zeros(point) for point in vertices]

    output = {
        'bounding_box': bounding_poly,
        'confidence': hint['confidence'],
        'importance_fraction': hint['importanceFraction']
    }

    return output


def _transform_landmark(landmark):
    bounding_box = get_in(['boundingPoly', 'vertices'], landmark)
    location = get_in(['locations', 0, 'latLng'], landmark)

    output = {
        'description': landmark['description'],
        'score': landmark['score'],
        'bounding_box': bounding_box,
        'location': location
    }
    return output


def ident_landmarks(image_url: str) -> Any:
    payload = {"requests": [
        {"image": {"source": {"imageUri": image_url}}, "features": [{"type": "LANDMARK_DETECTION"}],
         },
    ]}
    response = post_google_vision_endpoint(payload=payload)
    landmark_annotations = get_in(['responses', 0, 'landmarkAnnotations'], response)
    if landmark_annotations is not None:
        landmarks = list(map(_transform_landmark, landmark_annotations))
    else:
        landmarks = []
    output = {'landmarks': landmarks}
    return output


def func_w_no_annotations(a):
    pass


def func_w_no_params():
    return 1


def func_w_optional_annotations(a: Optional[int], b: Optional[CropHintAnnotation]) -> Optional[CropHintAnnotation]:
    pass


def func_w_lists(a: List[int], b: List[int]) -> List[CropHintAnnotation]:
    pass


def func_w_optional_lists(a: Optional[List[int]], b: Optional[List[int]]) -> Optional[List[CropHintAnnotation]]:
    pass


def func_w_optional_elements(a: List[Optional[int]], b: List[Optional[CropHintAnnotation]]) -> List[
    Optional[CropHintAnnotation]]:
    pass


def func_w_optional_iterable(a: Iterable[Optional[int]], b: Iterable[Optional[CropHintAnnotation]]) -> Iterable[
    Optional[CropHintAnnotation]]:
    pass


def func_w_optional_sequence(a: Sequence[Optional[int]], b: Sequence[Optional[CropHintAnnotation]]) -> Iterable[
    Optional[CropHintAnnotation]]:
    pass


FUNCTIONS = [ident_landmarks, ident_crop_hints, ident_dominant_colors,
             func_w_no_annotations, func_w_no_params, func_w_optional_annotations,
             func_w_lists, func_w_optional_elements, func_w_optional_lists, func_w_optional_iterable,
             func_w_optional_sequence]
