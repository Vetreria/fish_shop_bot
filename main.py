import os
import json
import requests
import dotenv

def fetch_api_token(ep_client, ep_secret):
    data = {
    'client_id': ep_client,
    'client_secret':  ep_secret,
    'grant_type': 'client_credentials',
    }
    response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    response.raise_for_status()
    return response.json()


def add_to_cart(api_token, item_id = 'd96a36df-06d3-4e90-a3f6-b8860ad81256', count = 1):
    headers = {
    'Authorization': api_token,
    }

    json_data = {
        'data': {
        'id': item_id,
        'type': 'cart_item',
        'quantity': count,
            },
    }
    response = requests.post('https://api.moltin.com/v2/carts/:reference/items', headers=headers, json=json_data)
    response.raise_for_status()
    print(response.json())


def get_products(api_token):
    headers = {
    'Authorization': api_token,
    }
    response = requests.get('https://api.moltin.com/v2/products', headers=headers)
    response.raise_for_status()
    return response.json()['data']


def get_cart(api_token):
    headers = {
    'Authorization': api_token,
    }
    response = requests.get('https://api.moltin.com/v2/carts/:reference', headers=headers)
    response.raise_for_status()
    print(response.json())





def main():
    dotenv.load_dotenv()
    ep_store = os.environ["ELASTIC_STORE_ID"]
    ep_client = os.environ["ELASTIC_CLIENT_ID"]
    ep_secret = os.environ["ELASTIC_CLIENT_SECRET"]
    api_token_result = fetch_api_token(ep_client, ep_secret)
    api_token = f"{api_token_result['token_type']} {api_token_result['access_token']}"
    get_products(api_token)
    # add_to_cart(api_token)
    # get_cart(api_token)






if __name__ == "__main__":
    main()