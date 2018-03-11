from django.contrib import admin
from .models import Vacancy, Company, City


class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']


class CityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(City, CityAdmin)
