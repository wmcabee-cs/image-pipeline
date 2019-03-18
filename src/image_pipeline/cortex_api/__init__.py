from cortex_client import OutputMessage, DatasetsClient
import jsonlines
import dill
import base64
import pandas as pd


class CortexAPI(object):

    @staticmethod
    def get_inputs(params, item):
        payload = params.get('payload')
        if payload is None:
            return None

        # if name is None, then return entire payload
        if item is None:
            return payload

        print('payload:', sorted(payload))
        if item not in payload:
            raise Exception(f"Item '{item}' not found in payload. Available items {sorted(payload)}. ")
        value = payload.get(item)
        return value


    @staticmethod
    def encode_dataframe_message(df, name='df'):
        data = dill.dumps(df)
        data = base64.b64encode(data).decode()
        payload = {name: data}
        output = OutputMessage(payload=payload, type_name="cortex/text").to_params()
        return output

    @staticmethod
    def decode_dataframe_message(msg, name='df'):
        data = msg['payload'][name]
        data = base64.b64decode(data)
        df = dill.loads(data)
        return df


class LowLevelAPI(CortexAPI):

    @staticmethod
    def get_client(params):
        data_client = DatasetsClient(
            url=params['apiEndpoint'],
            version="3",
            token=params['token']

        )
        return data_client

    @staticmethod
    def get_dataframe(params, dataset_name):
        dataset_client = __class__.get_client(params)
        data = dataset_client.get_stream(dataset_name).read()
        data = data.decode().split("\n")
        reader = jsonlines.Reader(data)
        df = pd.DataFrame.from_records(iter(reader))
        return df


"""
class HighLevelAPI(CortexAPI):

    @staticmethod
    def get_client(params):
        client = Cortex.client(api_endpoint=params['apiEndpoint'], token=params['token'])
        return client

    @staticmethod
    def get_dataframe(params, dataset_name):
        client = __class__.get_client(params)
        ds = client.dataset(dataset_name)
        df = ds.as_pandas()
        return df
# API = HighLevelAPI
"""

API = LowLevelAPI


def main(params):
    # get input dataset
    ds_name = API.get_inputs(params, item='ds_name')
    df = API.get_dataframe(params, dataset_name=ds_name)
    output = API.encode_dataframe_message(df=df)
    return output
