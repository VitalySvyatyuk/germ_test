from rest_framework import serializers

from .models import Vacancy, Company, City


class LocationField(serializers.RelatedField):
    def to_representation(self, value):
        return value.location

    def get_queryset(self):
        return City.objects.all()


class CompanySerializer(serializers.ModelSerializer):
    location = LocationField()

    class Meta:
        model = Company
        fields = [
            'name',
            'location'
        ]


class VacancySerializer(serializers.ModelSerializer):
    location = LocationField()
    company = CompanySerializer()

    class Meta:
        model = Vacancy
        fields = [
            'is_active',
            'title',
            'location',
            'starts_at',
            'ends_at',
            'description',
            'image_list',
            'company'
        ]
