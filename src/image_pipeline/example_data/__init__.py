import os
from pathlib import Path
import pandas as pd

import cortex

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))


def get_test_images():
    infile = THIS_DIR / 'test_images.csv'
    print("image__url test dataset:", infile)
    df = pd.read_csv(infile)
    return df


def upload_test_images():
    """Load local dataset to cortex"""

    # Initialize client interfaces
    cortex_client = cortex.Cortex.client()

    # Create and set parameters for dataset builder object
    builder = cortex_client.builder()
    ds_builder = builder.dataset("bill/test_images")
    ds_builder.title('Bills test image dataset')

    # create cortex builder object from the csv file

    df = get_test_images()
    ds_builder.from_df(df)
    ds = ds_builder.build()
    print(f">> uploaded test dataset using current_profile: "
          f"name='{ds.name}', title='{ds.title}', infile='{INFILE}'.")
    return ds
