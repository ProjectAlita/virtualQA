import requests
import pytest
from os import environ

@pytest.fixture
def base_url():
    return environ.get('DEPLOYMENT_URL', "http://yourapiendpoint.com")

@pytest.mark.parametrize("name, birthDate, type, expected_status", [
    ("Fluffy", "2020-04-12", "Dog", 302),
    ("Whiskers", "2019-08-09", "Cat", 302),
    ("", "2020-04-12", "Dog", 400)
])
def test_create_pet(base_url, name, birthDate, type, expected_status):
    owner_id = 1 # Assuming owner with ID 1 exists for testing
    response = requests.post(f"{base_url}/owners/{owner_id}/pets/new", data={
        'name': name,
        'birthDate': birthDate,
        'type': type
    })
    assert response.status_code == expected_status

# Additional tests based on Gherkin scenarios will be implemented here.
# Tests for updating pets with valid and invalid data are to be added.
