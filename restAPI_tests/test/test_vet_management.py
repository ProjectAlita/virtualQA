import requests
import pytest
from os import environ

@pytest.fixture
def base_url():
    return environ.get('DEPLOYMENT_URL', "http://yourapiendpoint.com")

@pytest.mark.parametrize("format, endpoint", [
    ('HTML', '/vets.html'),
    ('JSON', '/vets.json'),
    ('XML', '/vets.xml')
])
def test_list_vets(base_url, format, endpoint):
    response = requests.get(f"{base_url}{endpoint}")
    assert response.status_code == 200
    if format == 'HTML':
        assert 'text/html' in response.headers['Content-Type']
    elif format == 'JSON':
        assert 'application/json' in response.headers['Content-Type']
        assert isinstance(response.json(), list)
    elif format == 'XML':
        assert 'application/xml' in response.headers['Content-Type']
        assert '<vets>' in response.text
