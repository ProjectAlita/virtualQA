import pytest
import requests
from os import environ

base_url = pytest.fixture(lambda: environ.get('DEPLOYMENT_URL', 'http://yourapiendpoint.com'))

class TestOwnerManagement:
    def setup_method(self, method):
        # Setup code here
        pass

    def teardown_method(self, method):
        # Teardown code here
        pass

    def test_initiate_creation_of_new_owner(self, base_url):
        response = requests.get(f'{base_url}/owners/new')
        assert response.status_code == 200
        assert 'owner creation form' in response.text

    @pytest.mark.parametrize('first_name, last_name, address, city, telephone', [
        ('John', 'Doe', '123 Main St.', 'Anytown', '1234567890')
    ])
    def test_process_creation_of_new_owner(self, base_url, first_name, last_name, address, city, telephone):
        owner_details = {'firstName': first_name, 'lastName': last_name, 'address': address, 'city': city, 'telephone': telephone}
        response = requests.post(f'{base_url}/owners/new', data=owner_details)
        assert response.status_code == 302
        # Redirection validation to be implemented

    def test_initiate_owner_search(self, base_url):
        response = requests.get(f'{base_url}/owners/find')
        assert response.status_code == 200
        assert 'owner search form' in response.text

    @pytest.mark.parametrize('last_name', ['Doe', 'Smith'])
    def test_process_find_owner_form(self, base_url, last_name):
        response = requests.get(f'{base_url}/owners', params={'lastName': last_name})
        assert response.status_code == 200
        # List or redirection validation to be implemented

    def test_initiate_update_of_owner(self, base_url):
        owner_id = '12345'
        response = requests.get(f'{base_url}/owners/{owner_id}/edit')
        assert response.status_code == 200
        assert 'owner update form' in response.text

    @pytest.mark.parametrize('owner_id, first_name, last_name, address, city, telephone', [
        ('12345', 'Jane', 'Roe', '456 Elm St.', 'Newtown', '0987654321')
    ])
    def test_process_update_of_owner(self, base_url, owner_id, first_name, last_name, address, city, telephone):
        updated_owner_details = {'firstName': first_name, 'lastName': last_name, 'address': address, 'city': city, 'telephone': telephone}
        response = requests.post(f'{base_url}/owners/{owner_id}/edit', data=updated_owner_details)
        assert response.status_code == 302
        # Redirection validation to be implemented

    def test_show_owner(self, base_url):
        owner_id = '12345'
        response = requests.get(f'{base_url}/owners/{owner_id}')
        assert response.status_code == 200
        assert 'details of the owner' in response.text
