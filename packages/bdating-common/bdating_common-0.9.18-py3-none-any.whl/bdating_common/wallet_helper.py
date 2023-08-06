import os
import requests

def get_matched_bdating_wallet_info(uid: str):
    endpoint = os.environ['BDATING_WALLET_API_ENDPOINT']
    endpoint_key = os.environ['BDATING_WALLET_API_KEY']
    return requests.get(
        url=f"{endpoint}match",
        params={
            'uid': uid,
        },
        headers={
            "x-api-key": endpoint_key
        }
    ).json()
