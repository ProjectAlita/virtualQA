import requests
import pytest
from os import environ

@pytest.fixture
def base_url():
    return environ.get('DEPLOYMENT_URL', "http://yourapiendpoint.com")

@pytest.mark.parametrize("firstName, lastName, address, city, telephone, expected_status", [
    ("John", "Doe", "123 Main St.", "Anytown", "1234567890", 201),
    ("Jane", "Roe", "456 Elm St.", "Newtown", "0987654321", 201),
    ("John", "", "123 Main St.", "Anytown", "1234567890", 400)
])
def test_create_owner(base_url, firstName, lastName, address, city, telephone, expected_status):
    response = requests.post(f"{base_url}/owners/new", data={
        'firstName': firstName,
        'lastName': lastName,
        'address': address,
        'city': city,
        'telephone': telephone
    })
    assert response.status_code == expected_status

# Additional tests based on Gherkin scenarios will be implemented here.
# Tests for finding owners, updating owner details, and displaying owner's details are to be added.
