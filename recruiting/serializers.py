from rest_framework import serializers

from .models import Vacancy, Company, City


class LocationField(serializers.RelatedField):
    def to_representation(self, value):
        return value.location

    def to_internal_value(self, data):
        city, status = City.objects.get_or_create(location=data)
        return city

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

    def to_internal_value(self, data):
        location, status = City.objects.get_or_create(location=data['location'])
        company, status = Company.objects.get_or_create(
            name=data['name'],
            location=location)
        return company


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

    def create(self, validated_data):
        return Vacancy.objects.create(**validated_data)
