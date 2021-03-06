from image_pipeline.cortex_api import LowLevelAPI as API
from image_pipeline.actions import a_ident_bounding_boxes


def main(params):
    # get input dataset
    df = API.decode_dataframe_message(params)
    df = a_ident_bounding_boxes(input=df)
    output = API.encode_dataframe_message(df=df)
    return output
