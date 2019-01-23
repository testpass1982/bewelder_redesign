import itertools

from django.contrib.auth import get_user_model
from django.test import TestCase

from resumes.models import Resume

User = get_user_model()


class ResumeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('foo@bar.com', first_name='Иван', last_name='Иванов')

    def test_str_resume(self):
        user = User.objects.first()
        resume = Resume.objects.create(user=user, position='Сварщик')
        expected = 'Резюме: сварщик Иван Иванов'
        result = str(resume)
        self.assertEqual(expected, result)

    def test_salary_property(self):
        user = User.objects.first()
        resume = Resume.objects.create(user=user, position='Сварщик')
        self.assertEqual(resume.salary, '')
        resume.salary_min = 50000
        self.assertEqual(resume.salary, 'от 50000')
        resume.salary_max = 100000
        self.assertEqual(resume.salary, '50000-100000')
        resume.salary_min = 0
        self.assertEqual(resume.salary, 'до 100000')

    def test_experience_str(self):
        user = User.objects.first()
        resume = Resume.objects.create(user=user, position='Сварщик')
        self.assertEqual(resume.experience_str, '0 лет')
        for i, exp in ((1, '1 год'), (21, '21 год'), (31, '31 год')):
            resume.experience = i
            with self.subTest(i=i):
                self.assertEqual(resume.experience_str, exp)
        
        for i in itertools.chain(range(5, 21), range(25, 31), range(35, 41)):
            resume.experience = i
            with self.subTest(i=i):
                self.assertEqual(resume.experience_str, '{} лет'.format(i))

        for i in itertools.chain(range(2, 5), range(22, 25), range(32, 35)):
            resume.experience = i
            with self.subTest(i=i):
                self.assertEqual(resume.experience_str, '{} года'.format(i))
