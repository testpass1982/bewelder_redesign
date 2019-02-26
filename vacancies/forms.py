from django import forms

from vacancies.models import Vacancy


class VacancyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vacancy
        exclude = ('user', 'employer', 'category', 'created_date')

class VacancySearchForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(forms.Form, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'

    business_trips = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))
    shifted_work = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))
    naks_att_required = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))
    naks_att_level1 = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))
    naks_att_level2 = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))
    naks_att_level3 = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))
    naks_att_level4 = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))
    salary_min = forms.IntegerField(label='Зарплата от', required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary_max = forms.IntegerField(label='Зарплата от', required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))