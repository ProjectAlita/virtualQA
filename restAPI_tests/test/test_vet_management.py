import pytest
import requests
from os import environ

@pytest.fixture(scope='module')
def base_url():
    return environ.get('DEPLOYMENT_URL', 'http://yourapiendpoint.com')

def setup_module(module):
    # Setup for the entire module
    pass

def teardown_module(module):
    # Teardown for the entire module
    pass

class TestVetManagement:
    def setup_method(self, method):
        # Setup for each test method
        pass

    def teardown_method(self, method):
        # Teardown for each test method
        pass

    @pytest.mark.parametrize('format, endpoint', [
        ('HTML', '/vets.html'),
        ('JSON', '/vets.json'),
        ('XML', '/vets.xml')
    ])
    def test_list_all_vets(self, base_url, format, endpoint):
        response = requests.get(f'{base_url}{endpoint}')
        assert response.status_code == 200
        if format == 'HTML':
            assert 'text/html' in response.headers['Content-Type']
        elif format == 'JSON':
            assert 'application/json' in response.headers['Content-Type']
        elif format == 'XML':
            assert 'application/xml' in response.headers['Content-Type']
