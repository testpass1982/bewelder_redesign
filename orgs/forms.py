from django import forms

from orgs.models import Employer, Region, City


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = '__all__'

    def clean(self):
        cleaned_data = super(EmployerForm, self).clean()

        if cleaned_data['short_name'] == '':
            cleaned_data['short_name'] = cleaned_data['name']

        return cleaned_data


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'
