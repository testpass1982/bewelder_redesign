from django.test import TestCase

from users.models import User, UserManager


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user('foo@BAR.com', 'passw')
        self.assertEqual(user.email, 'foo@bar.com')
        self.assertFalse(user.check_password('bad_passw'))
        self.assertTrue(user.check_password('passw'))

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_seeker)
        self.assertFalse(user.is_employer)

    def test_empty_email(self):
        self.assertRaisesMessage(ValueError,
                                 'User must have an email address',
                                 User.objects.create_user, email='')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser('super@foo.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class UserTestCase(TestCase):
    def test_user_clean(self):
        user = User(email='foo@BAR.com')
        user.clean()
        self.assertEqual(user.email, 'foo@bar.com')

    def test_user_get_full_name(self):
        user = User(email='foo@bar.com', first_name='Иван', last_name='Иванов')
        self.assertEqual(user.get_full_name(), 'Иван Иванов')

    def test_user_get_short_name(self):
        user = User(email='foo@bar.com', first_name='Иван', last_name='Иванов')
        self.assertEqual(user.get_short_name(), 'Иван И.')
