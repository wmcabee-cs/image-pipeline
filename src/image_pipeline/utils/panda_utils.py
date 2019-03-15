import pandas as pd


def dict2df(adict):
    return pd.DataFrame.from_records([adict])
