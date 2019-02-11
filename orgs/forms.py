from django import forms

from orgs.models import Employer, Region, City


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = '__all__'


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'
