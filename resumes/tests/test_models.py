from django.test import TestCase
from django.contrib.auth import get_user_model

from resumes.models import Resume


User = get_user_model()


class ResumeTestCase(TestCase):
    def test_str_resume(self):
        user = User.objects.create_user('foo@bar.com', first_name='Иван', last_name='Иванов')
        resume = Resume.objects.create(user=user, position='Сварщик')
        expected = 'Резюме: сварщик Иван Иванов'
        result = str(resume)
        self.assertEqual(expected, result)
