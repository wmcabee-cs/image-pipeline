import keyring
from requests.exceptions import HTTPError
import requests

API_KEY_GOOGLE = keyring.get_password('visual.google.api', 'api_key')
HEADERS = headers = {'content-type': "application/json"}


def post_google_vision_endpoint(payload):
    url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY_GOOGLE}"
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data
    except HTTPError as e:
        print(f'>> HTTP error when calling vision end point. payload={payload}')
        raise
