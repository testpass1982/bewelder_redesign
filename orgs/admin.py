from django.contrib import admin
from .models import Employer, City, Region


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass
