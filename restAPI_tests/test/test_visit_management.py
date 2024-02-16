import requests
import pytest
from os import environ

@pytest.fixture
def base_url():
    return environ.get('DEPLOYMENT_URL', "http://yourapiendpoint.com")

@pytest.mark.parametrize("date, description, expected_status", [
    ("2023-05-01", "Annual vaccination", 302),
    ("2023-06-15", "General checkup", 302),
    ("", "Checkup", 400)
])
def test_create_visit(base_url, date, description, expected_status):
    pet_id = 101 # Assuming pet with ID 101 exists for testing
    response = requests.post(f"{base_url}/owners/1/pets/{pet_id}/visits/new", data={
        'date': date,
        'description': description
    })
    assert response.status_code == expected_status

# Additional tests based on Gherkin scenarios will be implemented here.
# Tests for initiating a new visit form and showing all visits for a pet are to be added.
