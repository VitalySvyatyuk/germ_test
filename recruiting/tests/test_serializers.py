import json

import pytest
import requests
from requests.auth import HTTPBasicAuth

from recruiting.models import Vacancy

URL = 'https://mysterious-springs-82115.herokuapp.com/api/vacancies/'
USER = 'test_jobufo'
PASSWORD = 'test_jobufo'
HEADERS = {
    'User-Agent': 'Mozilla 5.0',
    'Content-Type': 'application/json'}


def test_get_request():
    response = requests.get(URL)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'


@pytest.mark.django_db(transaction=True)
def test_post_request():
    request_body = {
        'is_active': False,
        'title': 'new Fresh Vacancy',
        'location': 'Hannover',
        'starts_at': 'Jederzeit',
        'ends_at': 'keine Angabe',
        'description': 'Some looooooooooooong description',
        'image_list': [
            'https://www.google.com/img2.png'],
        'company': {
            'name': 'Sixt',
            'location': 'Hannover'}}
    request_json = json.dumps(request_body)
    response = requests.post(URL,
        request_json,
        headers=HEADERS,
        auth=HTTPBasicAuth(USER, PASSWORD))
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'

    # Remove test query from DB
    Vacancy.objects.filter(title="new Fresh Vacancy").delete()
