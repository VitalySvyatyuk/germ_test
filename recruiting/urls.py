from django.conf.urls import url
from recruiting.views import VacancyListView

urlpatterns = [
    url(r'^vacancies/$', VacancyListView.as_view(), name='vacancy-all'),
]
