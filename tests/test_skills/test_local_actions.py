import os
from pathlib import Path
import pandas as pd
from importlib import import_module, invalidate_caches
from image_pipeline.utils import debug_utils



def test_local_pipeline():
    ident_colors = debug_utils.load_skill_module('ident_colors')
    ident_bounding_boxes = debug_utils.load_skill_module('ident_bounding_boxes')
    ident_landmarks = debug_utils.load_skill_module('ident_landmarks')


    # IDENTIFY COLORS SKILL
    colors_msg= debug_utils.call_cortex_function(ident_colors.main, payload={'ds_name': 'bill/test_images'})
    df = ident_colors.API.decode_dataframe_message(colors_msg)

    # IDENTIFY COLORS SKILL
    bounding_boxes_msg = debug_utils.call_cortex_function(ident_bounding_boxes.main, payload=colors_msg['payload'])
    df = ident_bounding_boxes.API.decode_dataframe_message(bounding_boxes_msg)

    # IDENTIFY LANDMARKS SKILL
    landmarks_msg = debug_utils.call_cortex_function(ident_landmarks.main, payload=bounding_boxes_msg['payload'])
    df = ident_landmarks.API.decode_dataframe_message(landmarks_msg)
    assert type(df) == pd.DataFrame


