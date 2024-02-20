import pytest
import requests
from os import environ

base_url = pytest.fixture(lambda: environ.get('DEPLOYMENT_URL', 'http://yourapiendpoint.com'))

class TestVisitManagement:
    def setup_method(self, method):
        # Setup code here
        pass

    def teardown_method(self, method):
        # Teardown code here
        pass

    def test_initiate_creation_of_new_visit(self, base_url):
        pet_id = '67890'
        response = requests.get(f'{base_url}/owners/*/pets/{pet_id}/visits/new')
        assert response.status_code == 200
        assert 'visit creation form' in response.text

    @pytest.mark.parametrize('owner_id, pet_id, date, description', [
        ('12345', '67890', '2023-04-12', 'Annual vaccination')
    ])
    def test_process_creation_of_new_visit(self, base_url, owner_id, pet_id, date, description):
        visit_details = {'date': date, 'description': description}
        response = requests.post(f'{base_url}/owners/{owner_id}/pets/{pet_id}/visits/new', data=visit_details)
        assert response.status_code == 302
        assert response.headers.get('Location').endswith(f'/owners/{owner_id}')

    def test_show_visits_for_pet(self, base_url):
        pet_id = '67890'
        response = requests.get(f'{base_url}/owners/*/pets/{pet_id}/visits')
        assert response.status_code == 200
        assert 'list of visits for the pet' in response.text
