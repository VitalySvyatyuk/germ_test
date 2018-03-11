from django.db.models import Q
from rest_framework import generics, mixins

from .models import Vacancy
from .serializers import VacancySerializer


class VacancyListView(mixins.CreateModelMixin, mixins.UpdateModelMixin, generics.ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        qs = Vacancy.objects.filter(is_active=True)
        q_location = self.request.GET.get("location")
        q_company = self.request.GET.get("company")
        if q_location and q_company:
            qs = qs.filter(Q(location__location__icontains=q_location)&Q(company__name__icontains=q_company)).distinct()
        elif q_location and not q_company:
            qs = qs.filter(location__location__icontains=q_location)
        elif q_company and not q_location:
            qs = qs.filter(company__name__icontains=q_company)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
