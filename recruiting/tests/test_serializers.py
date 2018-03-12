import pytest

from rest_framework.test import APIRequestFactory, \
    force_authenticate, RequestsClient
from django.contrib.auth.models import AnonymousUser, User
from recruiting.views import VacancyListView

URL = 'https://mysterious-springs-82115.herokuapp.com/api/vacancies'


@pytest.mark.django_db(transaction=True)
def test_get_request(rf):
    global USER
    USER = User.objects.filter(username='test_jobufo')
    factory = APIRequestFactory()

    request = rf.get('/api/vacancies/')
    # request.user = USER
    response = VacancyListView.as_view()(request)

    # client = RequestsClient()
    # response = client.get('api/vacancies')
    import pdb; pdb.set_trace()
    assert response.status_code == 200


def test_post_request():
    factory = APIRequestFactory()
    request = factory.post('/api/vacancies/', {
        'is_active': 'true',
        'title': 'new Fresh Vacancy',
        'location': 'Hannover',
        'starts_at': 'Jederzeit',
        'ends_at': 'keine Angabe',
        'description': 'Some looooooooooooong description',
        'image_list': ['https://www.google.com/img2.png'],
        'company': {
            'name': 'Sixt',
            'location': 'Hannover'}},
        format='json')


"""           
{
    'is_active': false,
    'title': '',
    'location': null,
    'starts_at': '',
    'ends_at': '',
    'description': '',
    'image_list': [],
    'company': {
        'name': '',
        'location': null
    }
}
"""