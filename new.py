import json
import requests


def conv_bytes_to_json(bytes_data):
    return json.loads(bytes_data.decode('utf-8'))


add_pet_headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

add_image_headers = {
    'accept': 'application/json',
    'Content-Type': 'multipart/form-data'
}
get_pet_headers = {
    'accept': 'application/json'
}

update_pet_headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

delete_pet_headers = {
    'accept': 'application/json',
    'api-key': 'special-key'
}

def get_pet_body(kwargs):
    body = {
        "name": "Alf",
        "photoUrls": []
    }
    body = {**body, **kwargs}
    return json.dumps(body)


# def test_add_pet_wrong_structure():
#     pet = get_pet_body({'hobby': 'running'})
#     url = 'https://petstore.swagger.io/v2/pet'
#     response = requests.post(url, data=pet, headers=add_pet_headers)
#     id = conv_bytes_to_json(response.content)['id']
#     print(id)
#     assert response.status_code == 405


def test_add_pet_existing_id():
    pet = get_pet_body({})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    id = conv_bytes_to_json(response.content)['id']
    new_pet = get_pet_body({'id': id, 'name': 'snowball'})
    response = requests.post(url, data=new_pet, headers=add_pet_headers)
    assert response.status_code == 400



test_add_pet_existing_id()
