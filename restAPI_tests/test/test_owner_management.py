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

class TestOwnerManagement:
    def setup_method(self, method):
        # Setup for each test method
        pass

    def teardown_method(self, method):
        # Teardown for each test method
        pass

    @pytest.mark.parametrize('firstName, lastName, address, city, telephone', [
        ('John', 'Doe', '123 Main St.', 'Anytown', '1234567890'),
        ('Jane', 'Roe', '456 Elm St.', 'Newtown', '0987654321')
    ])
    def test_create_owner_with_valid_data(self, base_url, firstName, lastName, address, city, telephone):
        # Test implementation
        pass

    def test_create_owner_with_missing_required_fields(self, base_url):
        # Test implementation
        pass

    def test_find_owner_with_existing_last_name(self, base_url):
        # Test implementation
        pass

    def test_find_owner_with_non_existing_last_name(self, base_url):
        # Test implementation
        pass

    @pytest.mark.parametrize('ownerId, firstName, lastName, address, city, telephone', [
        (1, 'John', 'Smith', '123 Main St.', 'Anytown', '1234567890'),
        (2, 'Jane', 'Doe', '456 Elm St.', 'Newtown', '0987654321')
    ])
    def test_update_owner_with_valid_data(self, base_url, ownerId, firstName, lastName, address, city, telephone):
        # Test implementation
        pass

    def test_update_owner_with_invalid_data(self, base_url):
        # Test implementation
        pass

    def test_display_existing_owner_details(self, base_url):
        # Test implementation
        pass
