import pytest
import requests
from os import environ

base_url = pytest.fixture(lambda: environ.get('DEPLOYMENT_URL', 'http://yourapiendpoint.com'))

class TestPetManagement:
    def setup_method(self, method):
        # Setup code here
        pass

    def teardown_method(self, method):
        # Teardown code here
        pass

    def test_initiate_creation_of_new_pet(self, base_url):
        owner_id = '12345'
        response = requests.get(f'{base_url}/owners/{owner_id}/pets/new')
        assert response.status_code == 200
        assert 'pet creation form' in response.text

    @pytest.mark.parametrize('owner_id, name, birth_date, type', [
        ('12345', 'Bella', '2020-04-23', 'Dog')
    ])
    def test_process_creation_of_new_pet(self, base_url, owner_id, name, birth_date, type):
        pet_details = {'name': name, 'birthDate': birth_date, 'type': type}
        response = requests.post(f'{base_url}/owners/{owner_id}/pets/new', data=pet_details)
        assert response.status_code == 302
        assert response.headers.get('Location').endswith(f'/owners/{owner_id}')

    def test_initiate_update_of_pet(self, base_url):
        owner_id = '12345'
        pet_id = '67890'
        response = requests.get(f'{base_url}/owners/{owner_id}/pets/{pet_id}/edit')
        assert response.status_code == 200
        assert 'pet update form' in response.text

    @pytest.mark.parametrize('owner_id, pet_id, name, birth_date, type', [
        ('12345', '67890', 'Max', '2019-05-30', 'Cat')
    ])
    def test_process_update_of_pet(self, base_url, owner_id, pet_id, name, birth_date, type):
        updated_pet_details = {'name': name, 'birthDate': birth_date, 'type': type}
        response = requests.post(f'{base_url}/owners/{owner_id}/pets/{pet_id}/edit', data=updated_pet_details)
        assert response.status_code == 302
        assert response.headers.get('Location').endswith(f'/owners/{owner_id}')
