import requests
from pydantic import UrlStr
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError
import requests
from toolz import get_in, assoc, take
from typing import List, Any, Optional
import keyring

API_KEY_GOOGLE = keyring.get_password('visual.google.api', 'api_key')
IMAGE_URL = r'https://www.kids-world-travel-guide.com/images/xparis_eiffeltower_ssk500.jpeg.pagespeed.ic.2lwZPZtnJ8.jpg'
HEADERS = headers = {'content-type': "application/json"}


###################################################
# Data Types
###################################################
@dataclass
class ColorRGB:
    red: int
    green: int
    blue: int


@dataclass
class DominentColor:
    color: ColorRGB
    score: float
    pixelFraction: float


#######################################
# Helper functions
#######################################

def _add_zeros(point):
    point['x'] = point.get('x', 0)
    point['y'] = point.get('y', 0)
    return point


def _post_google_vision_endpoint(payload):
    url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY_GOOGLE}"
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data
    except HTTPError as e:
        print(f'>> HTTP error when calling ident_colors, payload={payload}')
        raise


##############################################
# Web services
##############################################
def ident_colors(image_url: str, limit: Optional[int]) -> List[DominentColor]:
    payload = {"requests": [
        {"image": {"source": {"imageUri": image_url}}, "features": [{"type": "IMAGE_PROPERTIES"}]},
    ]}
    data = _post_google_vision_endpoint(payload=payload)
    reader = get_in(['responses', 0, 'imagePropertiesAnnotation', 'dominantColors', 'colors'], data)
    reader = sorted(reader, key=lambda x: x['score'], reverse=True)
    if limit is not None:
        reader = list(take(limit, reader))
    reader = list(reader)
    ret = {'colors': reader}
    return ret


def ident_bounding_box(image_url: str, aspect_ratios: Optional[float] = 1.0) -> Any:
    if aspect_ratios is not None:
        aspect_ratios = [aspect_ratios]
    payload = {"requests": [
        {"image": {"source": {"imageUri": image_url}}, "features": [{"type": "CROP_HINTS"}],
         'imageContext': {'cropHintsParams': {'aspectRatios': [aspect_ratios]}},
         },
    ]}
    response = _post_google_vision_endpoint(payload=payload)
    hint = get_in(['responses', 0, 'cropHintsAnnotation', 'cropHints', 0], response)

    #########################
    # build boundingBox item
    #  - promote 'vertices' item to top level object
    #  - google api does not return x, y values when zero. Add zeros to vertices pairs where missing
    vertices = get_in(['boundingPoly', 'vertices'], hint)
    bounding_poly = [_add_zeros(point) for point in vertices]

    output = {
        'boundingPoly': bounding_poly,
        'confidence': hint['confidence'],
        'importanceFraction': hint['importanceFraction']
    }

    return output

def ident_landmarks(image_url: str) -> Any:
    payload = {"requests": [
        {"image": {"source": {"imageUri": image_url}}, "features": [{"type": "LANDMARK_DETECTION"}],
         },
    ]}
    response = _post_google_vision_endpoint(payload=payload)
    landmark_annotations = get_in(['responses', 0, 'landmarkAnnotations'], response)
    ret ={ 'landmark_annotations': landmark_annotations }
    return ret
