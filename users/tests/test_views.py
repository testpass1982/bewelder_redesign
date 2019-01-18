from django.test import TestCase
from django.urls import reverse

from users.models import User


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
        self.assertRedirects(resp, reverse('users:login'))
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


class UserLoginViewTestCase(TestCase):
    def test_login_url_accessible(self):
        resp = self.client.get(reverse('users:login'))
        self.assertEqual(resp.status_code, 200)

    def test_user_can_login(self):
        user = User.objects.create_user('user123@foo.bar', 'password')
        resp = self.client.post(reverse('users:login'), {
            'username': 'bad_user@foo.bar',
            'password': 'password',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(
            resp, 'Пожалуйста, введите правильные email и пароль. Оба поля могут быть чувствительны к регистру.')

        resp = self.client.post(reverse('users:login'), {
            'username': 'user123@foo.bar',
            'password': 'password',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/')


class UserLogoutViewTestCase(TestCase):
    def test_logout_url_accessible(self):
        resp = self.client.get(reverse('users:logout'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')


class UserUpdateViewTestCase(TestCase):

    def test_profile_update(self):
        username = 'user@foo.bar'
        password = 'password'
        user = User.objects.create_user(username, password)
        self.client.login(username=username, password=password)
        resp = self.client.get(reverse('users:profile_update'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/profile_update.html')
        self.assertEqual(resp.context['user'], user)
        self.assertEqual(resp.context['user'].first_name, '')

        resp = self.client.post(
            reverse('users:profile_update'),
            {
                'email': 'new@mail.foo',
                'first_name': 'foo',
                'last_name': 'bar',
            }
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')
        user.refresh_from_db()
        self.assertEqual(user.email, 'new@mail.foo')
        self.assertEqual(user.first_name, 'foo')
        self.assertEqual(user.last_name, 'bar')

    def test_profile_update_unauthorized(self):
        resp = self.client.get(reverse('users:profile_update'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
            resp,
            '{}?next={}'.format(reverse('users:login'), reverse('users:profile_update'))
        )

        resp = self.client.post(reverse('users:profile_update'), {})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
            resp,
            '{}?next={}'.format(reverse('users:login'), reverse('users:profile_update'))
        )

class ChangePasswordViewTestCase(TestCase):

    def test_password_change(self):
        username = 'user@foo.bar'
        password = 'password'
        user = User.objects.create_user(username, password)
        self.client.login(username=username, password=password)
        resp = self.client.get(reverse('users:password_change'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/password_change.html')

    def test_password_change_unauthorized(self):
        resp = self.client.get(reverse('users:password_change'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
            resp,
            '{}?next={}'.format(reverse('users:login'), reverse('users:password_change'))
        )

        resp = self.client.post(reverse('users:password_change'), {})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
            resp,
            '{}?next={}'.format(reverse('users:login'), reverse('users:password_change'))
        )