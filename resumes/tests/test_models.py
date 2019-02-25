import itertools

from django.contrib.auth import get_user_model
from django.test import TestCase

from resumes.models import Resume

User = get_user_model()


class ResumeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('foo@bar.com', first_name='Иван', last_name='Иванов')
        self.resume = Resume.objects.create(user=self.user, position='Сварщик')
        

    def test_str_resume(self):
        expected = 'Резюме: сварщик Иван Иванов'
        result = str(self.resume)
        self.assertEqual(expected, result)

    def test_salary_property(self):
        self.assertEqual(self.resume.salary, '')
        self.resume.salary_min = 50000
        self.assertEqual(self.resume.salary, 'от 50000')
        self.resume.salary_max = 100000
        self.assertEqual(self.resume.salary, '50000-100000')
        self.resume.salary_min = 0
        self.assertEqual(self.resume.salary, 'до 100000')

    def test_experience_str(self):
        self.assertEqual(self.resume.experience_str, '0 лет')
        for i, exp in ((1, '1 год'), (21, '21 год'), (31, '31 год')):
            self.resume.experience = i
            with self.subTest(i=i):
                self.assertEqual(self.resume.experience_str, exp)
        
        for i in itertools.chain(range(5, 21), range(25, 31), range(35, 41)):
            self.resume.experience = i
            with self.subTest(i=i):
                self.assertEqual(self.resume.experience_str, '{} лет'.format(i))

        for i in itertools.chain(range(2, 5), range(22, 25), range(32, 35)):
            self.resume.experience = i
            with self.subTest(i=i):
                self.assertEqual(self.resume.experience_str, '{} года'.format(i))

    def test_get_absolute_url(self):
        result = self.resume.get_absolute_url()
        self.assertEqual(result, '/resumes/{}'.format(self.resume.id))
