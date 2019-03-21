from dataclasses import asdict
import pandas as pd
from typing import Dict

from image_pipeline import ml_module


# TODO: How to check datatype of pd.DataFrame, included nested datastructures (input, output)


# Load data
def a_load_data(request: Dict):
    df = pd.read_csv(request['path'])
    return df


# Identify colors
def a_ident_colors(input: pd.DataFrame) -> pd.DataFrame:
    return input.assign(dominant_colors=input.image_url.map(ml_module.ident_colors))


# Identify bounding boxes
def a_ident_bounding_boxes(input: pd.DataFrame) -> pd.DataFrame:
    return input.assign(bounding_boxes=input.image_url.map(ml_module.ident_bounding_boxes))


# Identify landmarks
def a_ident_landmarks(input: pd.DataFrame) -> pd.DataFrame:
    return input.assign(landmarks=input.image_url.map(ml_module.ident_landmarks))


def a_write_json(input: pd.DataFrame, request: Dict) -> pd.DataFrame:
    outfile = request['outfile']
    input.to_json(outfile, orient='records', lines=True)
    print('wrote %s' % str(outfile))
    return input
