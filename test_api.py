import json

import pytest
import requests

CREATE_HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

GET_HEADERS = {
    'accept': 'application/json'
}
UPDATE_HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

DELETE_HEADERS = {
    'accept': 'application/json',
    'api-key': 'special-key'
}

BASE_URL = 'https://petstore.swagger.io/v2/pet'


def conv_bytes_to_json(bytes_data):
    return json.loads(bytes_data.decode('utf-8'))


def _create_pet_body(kwargs):
    body = {
        "name": "Alf",
        "photoUrls": []
    }
    body = {**body, **kwargs}
    return json.dumps(body)


def _read_pet(pet_id):
    response = requests.get(f'{BASE_URL}/{pet_id}', headers=GET_HEADERS)
    data = conv_bytes_to_json(response.content)
    return data, response.status_code


def _update_pet(pet_id, data):
    response = requests.post(f'{BASE_URL}/{pet_id}', data=data, headers=GET_HEADERS)
    return response.status_code


def _delete_pet(pet_id):
    response = requests.delete(f'{BASE_URL}/{pet_id}', headers=DELETE_HEADERS)
    return response.status_code


@pytest.fixture
def pet():
    pet = _create_pet_body({})
    response = requests.post(BASE_URL, data=pet, headers=CREATE_HEADERS)

    data = conv_bytes_to_json(response.content)
    yield data

    _delete_pet(data['id'])


def test_add_pet():
    pet = _create_pet_body({})
    response = requests.post(BASE_URL, data=pet, headers=CREATE_HEADERS)
    assert response.status_code == 200
    object_id = conv_bytes_to_json(response.content)['id']
    content, status_code = _read_pet(object_id)
    assert status_code == 200
    assert content['name'] == 'Alf'
    _delete_pet(object_id)


def test_add_pet_existing_id(pet):
    object_id = pet['id']
    new_pet = _create_pet_body({'id': object_id, 'name': 'snowball'})
    response = requests.post(BASE_URL, data=new_pet, headers=CREATE_HEADERS)
    assert response.status_code == 400


def test_add_pet_negative_id():
    pet = _create_pet_body({'id': -1})
    response = requests.post(BASE_URL, data=pet, headers=CREATE_HEADERS)
    assert response.status_code == 405


def test_add_pet_wrong_status():
    pet = _create_pet_body({'status': 'Hello'})
    response = requests.post(BASE_URL, data=pet, headers=CREATE_HEADERS)
    assert response.status_code == 405


def test_upload_image(pet):
    object_id = pet['id']
    url = f'{BASE_URL}/{pet["id"]}/uploadImage'
    file = open("nuhler.jpeg", "rb")
    upload_response = requests.post(url, files={'file': file})
    assert upload_response.status_code == 200
    updated_object, status_code = _read_pet(object_id)
    assert status_code == 200
    assert pet['photoUrls'] != updated_object['photoUrls']


def test_update_pet(pet):
    object_id = pet['id']
    data = {
        'id': object_id,
        'name': 'Fluffy',
        'status': 'sold'
    }
    status_code = _update_pet(object_id, data)
    assert status_code == 200
    pet, status_code = _read_pet(pet['id'])
    assert pet['name'] == 'Fluffy'
    assert pet['status'] == 'sold'


def test_update_non_existent_pet(pet):
    _delete_pet(pet['id'])
    data = {
        'id': pet['id'],
        'name': 'Fluffy',
        'status': 'sold'
    }
    status_code = _update_pet(pet['id'], data)
    assert status_code == 404


def test_delete_pet(pet):
    url = f'{BASE_URL}/{pet["id"]}'
    requests.delete(url, headers=DELETE_HEADERS)
    data, status_code = _read_pet(pet["id"])
    assert status_code == 404


def test_delete_non_existent_pet(pet):
    _delete_pet(pet['id'])
    status_code = _delete_pet(pet['id'])
    assert status_code == 400


def test_delete_pet_without_api_key(pet):
    url = f'{BASE_URL}/{pet["id"]}'
    response = requests.delete(url, headers={'accept': 'application/json'})
    assert response.status_code == 405
