import os
import requests
import dotenv


def get_image_url(ep_api_token, image_id):
    headers = {
        'Authorization': ep_api_token,
    }
    response = requests.get(
        f'https://api.moltin.com/v2/files/{image_id}', headers=headers)
    response.raise_for_status()
    return response.json()['data']['link']['href']


def fetch_api_token(ep_client, ep_secret):
    data = {
        'client_id': ep_client,
        'client_secret':  ep_secret,
        'grant_type': 'client_credentials',
    }
    response = requests.post(
        'https://api.moltin.com/oauth/access_token', data=data)
    response.raise_for_status()
    print(response.json())
    return response.json()


def add_to_cart(ep_api_token, item_id, quantity, cart_id):
    headers = {
        'Authorization': ep_api_token,
        'Content-Type': 'application/json',
    }
    payload = {
        'data': {
            'id': item_id,
            'type': 'cart_item',
            'quantity': int(quantity)}}
    url = f'https://api.moltin.com/v2/carts/:{cart_id}/items'
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['data']


def get_products_in_cart(ep_api_token, cart_id):
    headers = {
        'Authorization': ep_api_token,
        'Content-Type': 'application/json',
    }
    url = f'https://api.moltin.com/v2/carts/:{cart_id}/items'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']


def get_products(ep_api_token):
    headers = {
        'Authorization': ep_api_token,
    }
    response = requests.get(
        'https://api.moltin.com/v2/products', headers=headers)
    response.raise_for_status()
    return response.json()['data']


def get_product(ep_api_token, product_id):
    headers = {
        'Authorization': ep_api_token,
    }
    response = requests.get(f'https://api.moltin.com/v2/products/{product_id}',
                            headers=headers)
    response.raise_for_status()
    return response.json()['data']


def get_cart(ep_api_token, cart_id):
    headers = {
        'Authorization': ep_api_token,
    }
    response = requests.get(
        f'https://api.moltin.com/v2/carts/:{cart_id}', headers=headers)
    response.raise_for_status()
    return response.json()


def delete_cart_item(ep_api_token, cart_id, product_id):
    headers = {
        'Authorization': ep_api_token,
    }
    url = f"https://api.moltin.com/v2/carts/:{cart_id}/items/{product_id}"
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.json()


def create_customer(ep_api_token, user_name, user_email):
    headers = {
        'Authorization': ep_api_token,
    }
    url = "https://api.moltin.com/v2/customers"
    payload = {
        "data": {
            "type": "customer",
            "name": user_name,
            "email": user_email}}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return (f""" 
    ID: {response.json()['data']['id']}
    Name(tg_chat): {response.json()['data']['name']}
    email: {response.json()['data']['email']}
    """)


def main():
    dotenv.load_dotenv()
    ep_store = os.environ["ELASTIC_STORE_ID"]
    ep_client = os.environ["ELASTIC_CLIENT_ID"]
    ep_secret = os.environ["ELASTIC_CLIENT_SECRET"]
    ep_api_token_result = fetch_api_token(ep_client, ep_secret)
    ep_api_token = f"{ep_api_token_result['token_type']} {ep_api_token_result['access_token']}"


if __name__ == "__main__":
    main()
