from image_pipeline.cortex_api import LowLevelAPI as API
from image_pipeline.actions import a_ident_colors


def main(params):
    # get input dataset
    ds_name = API.get_inputs(params, item='ds_name')
    df = API.get_dataframe(params, dataset_name=ds_name)

    df = a_ident_colors(input=df)

    output = API.encode_dataframe_message(df=df)
    return output
