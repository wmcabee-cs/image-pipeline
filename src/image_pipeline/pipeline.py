from image_pipeline import schemas
from image_pipeline.utils.schema_utils import validate_request
from image_pipeline.utils.pipeline_utils import run_pipeline
from image_pipeline.utils.skill_utils import build_skill

from image_pipeline.actions import (a_load_data, a_ident_colors, a_ident_bounding_boxes, a_ident_landmarks,
                                    a_write_json)


def build():
    pipeline = [
        build_skill(func=a_load_data, add_fields=schemas.RawImage),
        build_skill(func=a_ident_colors, required_inputs=schemas.RawImage, add_fields=schemas.DominantColorList),
        build_skill(func=a_ident_bounding_boxes, required_inputs=schemas.RawImage, add_fields=schemas.BoundingBoxList),
        build_skill(func=a_ident_landmarks, required_inputs=schemas.RawImage, add_fields=schemas.LandmarkList),
        build_skill(func=a_write_json, required_inputs=schemas.AnnotatedImage),
    ]
    return pipeline


def run(pipeline, request):
    validate_request(schema=schemas.RequestParameters, request=request)
    df = run_pipeline(pipeline=pipeline, request=request)
    return df
