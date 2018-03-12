from django.db.models import Q
from rest_framework import generics

from .models import Vacancy
from .serializers import VacancySerializer


class VacancyListView(generics.ListCreateAPIView):
    serializer_class = VacancySerializer
    lookup_field = 'title'

    def get_queryset(self):
        qs = Vacancy.objects.filter(is_active=True)
        q_location = self.request.GET.get("location")
        q_company = self.request.GET.get("company")
        if q_location and q_company:
            qs = qs.filter(Q(location__location__icontains=q_location) &
                           Q(company__name__icontains=q_company)).distinct()
        elif q_location and not q_company:
            qs = qs.filter(location__location__icontains=q_location)
        elif q_company and not q_location:
            qs = qs.filter(company__name__icontains=q_company)
        return qs

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    #
    # def patch(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args, **kwargs)


