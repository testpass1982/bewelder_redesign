from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        labels = {
            'password1': 'пароль',
            'password2': 'повторите пароль',
            'first_name': 'имя',
            'last_name': 'фамилия',
            'date_of_birth': 'дата рождения',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('Пользователь с таким емайл уже зарегестрирован.')
        return email
