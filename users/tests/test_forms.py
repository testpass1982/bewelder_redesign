from django.test import TestCase

from users.forms import UserRegistrationForm
from users.models import User


class UserRegistrationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_user('user1@mail.com', 'password')

    def test_user_already_exists(self):
        data = {
            'email': 'user1@mail.com',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['email'].errors, ['Пользователь с таким емайл уже зарегестрирован.'])
        
    def test_user_names_enabled(self):
        data = {
            'email': 'foo@bar.com',
            'password1': 'sbAB35EHR-*/',
            'password2': 'sbAB35EHR-*/',
            'first_name': '',
            'last_name': '',
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['first_name'].errors, ['Обязательное поле.'])
        self.assertEqual(form['last_name'].errors, ['Обязательное поле.'])
        data['first_name'] = 'Иван'
        data['last_name'] = 'Иванов'
        form = UserRegistrationForm(data)
        self.assertTrue(form.is_valid())

    def test_user_save(self):
        data = {
            'email': 'foo@bar.com',
            'password1': 'sbAB35EHR-*/',
            'password2': 'sbAB35EHR-*/',
            'first_name': 'Иван',
            'last_name': 'Иванов',
        }
        form = UserRegistrationForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.instance.email, 'foo@bar.com')
        form.save()
        self.assertEqual(
            User.objects.get(id=form.instance.id).email,
            'foo@bar.com'
        )


