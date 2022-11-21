import requests


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
    return response.json()['token_type'], response.json()['access_token'], response.json()['expires_in']


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
