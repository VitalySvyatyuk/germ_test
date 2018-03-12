from django.db import models
from django.contrib.postgres.fields import ArrayField


class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    location = models.ForeignKey('City', on_delete=models.CASCADE)
    starts_at = models.CharField(max_length=200)
    ends_at = models.CharField(max_length=200)
    description = models.CharField(max_length=5000, blank=True, null=True)
    image_list = ArrayField(models.CharField(max_length=300, blank=True), default=[])
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'vacancies'

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=300)
    location = models.ForeignKey('City', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class City(models.Model):
    location = models.CharField(max_length=2000)

    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.location
