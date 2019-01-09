from django.test import TestCase

from users.models import User
from django.urls import reverse


class UserRegistrationViewTestCase(TestCase):
    def test_user_registration(self):
        reg_url = reverse('users:registration')
        resp = self.client.get(reg_url)
        self.assertEqual(resp.status_code, 200)

        data = {
            'email': 'foo@bar.com',
            'password1': 'sbAB35EHR-*/',
            'password2': 'sbAB35EHR-*/',
            'first_name': 'Иван',
            'last_name': 'Иванов',
        }

        resp = self.client.post(reg_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        created_user = User.objects.get(email=data['email'])
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.first_name, 'Иван')

    def test_missing_email(self):
        data = {
            'password1': 'sbAB35EHR-*/',
            'password2': 'sbAB35EHR-*/',
            'first_name': 'Иван',
            'last_name': 'Иванов',
        }
        resp = self.client.post(reverse('users:registration'), data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'email', 'Обязательное поле.')

    def test_missing_names(self):
        data = {
            'email': 'foo@bar.com',
            'password1': 'sbAB35EHR-*/',
            'password2': 'sbAB35EHR-*/',
            'first_name': '',
            'last_name': '',
        }
        resp = self.client.post(reverse('users:registration'), data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'first_name', 'Обязательное поле.')
        self.assertFormError(resp, 'form', 'last_name', 'Обязательное поле.')
