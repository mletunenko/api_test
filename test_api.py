import json
import requests


def conv_bytes_to_json(bytes_data):
    return json.loads(bytes_data.decode('utf-8'))


def get_pet_body(kwargs):
    body = {
        "name": "Alf",
        "photoUrls": []
    }
    body = {**body, **kwargs}
    return json.dumps(body)


add_pet_headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
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


def test_add_pet():
    pet = get_pet_body({})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    assert response.status_code == 200
    id = conv_bytes_to_json(response.content)['id']
    check_response = requests.get(f'https://petstore.swagger.io/v2/pet/{id}', headers=get_pet_headers)
    content = conv_bytes_to_json(check_response.content)
    assert content['name'] == 'Alf'

def test_add_pet_existing_id():
    pet = get_pet_body({})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    id = conv_bytes_to_json(response.content)['id']
    new_pet = get_pet_body({'id': id, 'name': 'snowball'})
    response = requests.post(url, data=new_pet, headers=add_pet_headers)
    assert response.status_code == 400

def test_add_pet_negative_id():
    pet = get_pet_body({'id': -1})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    assert response.status_code == 405


def test_add_pet_wrong_status():
    pet = get_pet_body({'status': 'Hello'})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    assert response.status_code == 405




def test_upload_image():
    pet = get_pet_body({})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    content = conv_bytes_to_json(response.content)
    id = content['id']
    photoUrls = content['photoUrls']
    url = f'https://petstore.swagger.io/v2/pet/{id}/uploadImage'
    file = open("nuhler.jpeg", "rb")
    test_response = requests.post(url, files={'file': file})
    assert test_response.status_code == 200
    check_response = requests.get(f'https://petstore.swagger.io/v2/pet/{id}', headers=get_pet_headers)
    content = conv_bytes_to_json(check_response.content)
    assert content['photoUrls'] != photoUrls


def test_update_pet():
    pet = get_pet_body({})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    id = conv_bytes_to_json(response.content)['id']
    url = f'https://petstore.swagger.io/v2/pet/'
    data = {
        'id': id,
        'name': 'Fluffy',
        'status': 'sold'
    }
    pet = get_pet_body(data)
    response = requests.put(url, data=pet, headers=add_pet_headers)
    content = conv_bytes_to_json(response.content)
    assert response.status_code == 200
    assert content['name'] == 'Fluffy'
    assert content['status'] == 'sold'

def test_update_non_existent_pet():
    pet = get_pet_body({})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    id = conv_bytes_to_json(response.content)['id']
    url = f'https://petstore.swagger.io/v2/pet/{id}'
    requests.delete(url, headers=delete_pet_headers)
    url = f'https://petstore.swagger.io/v2/pet/'
    data = {
        'id': id,
        'name': 'Fluffy',
        'status': 'sold'
    }
    pet = get_pet_body(data)
    response = requests.put(url, data=pet, headers=add_pet_headers)
    assert response.status_code == 404


def test_delete_pet():
    pet = get_pet_body({})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    id = conv_bytes_to_json(response.content)['id']
    url = f'https://petstore.swagger.io/v2/pet/{id}'
    requests.delete(url, headers=delete_pet_headers)
    response = requests.get(f'https://petstore.swagger.io/v2/pet/{id}', headers=get_pet_headers)
    assert response.status_code == 404

def test_delete_non_existent_pet():
    pet = get_pet_body({})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    id = conv_bytes_to_json(response.content)['id']
    url = f'https://petstore.swagger.io/v2/pet/{id}'
    requests.delete(url, headers=delete_pet_headers)
    response = requests.delete(url, headers=delete_pet_headers)
    assert response.status_code == 404

def test_delete_pet_without_api_key():
    pet = get_pet_body({})
    url = 'https://petstore.swagger.io/v2/pet'
    response = requests.post(url, data=pet, headers=add_pet_headers)
    id = conv_bytes_to_json(response.content)['id']
    url = f'https://petstore.swagger.io/v2/pet/{id}'
    response = requests.delete(url, headers={'accept': 'application/json'})
    assert response.status_code == 405