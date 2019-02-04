from django.test import TestCase
from django.test import Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from vacancies.views import vacancies_list
from vacancies.models import Vacancy, Level
from django.core.paginator import Paginator
from orgs.models import Employer, City, Region
from users.models import User
from http import HTTPStatus
from vacancies.forms import VacancyForm
from django.shortcuts import get_object_or_404
from mixer.backend.django import mixer
import random

# Create your tests here.

# class SmokeTest(TestCase):

#     def test_bad_maths(self):
#         self.assertEqual(1+1, 3)

class VacancyModelTest(TestCase):

    def setUp(self):
        region_test_data = {
            'name' : 'MO'
            }
        mo_region = Region.objects.create(**region_test_data)
        city_test_data = {
            'name': 'MOSCOW',
            'region': mo_region
            }
        moscow = City.objects.create(**city_test_data)
        employer_test_data = {
            'name': 'LUKOIL',
            'short_name': 'LUK',
            'inn': '123456789012',
            'city': moscow,
            'phone': '123',
            'email': 'test_email@test.com'
            }
        self.employer = Employer.objects.create(**employer_test_data)

    def test_saving_and_retrieving_vacancies(self):
        username1 = 'foo1@bar.com'
        password = 'geekbrains'
        user1 = User.objects.create_user(username1, password)
        first_vacancy = Vacancy()
        first_vacancy.user = user1
        first_vacancy.employer = self.employer
        first_vacancy.title = 'Welder TIG'
        first_vacancy.salary_min = 50000 
        first_vacancy.save()

        second_vacancy = Vacancy()
        username2 = 'foo2@bar.com'
        password = 'geekbrains'
        user2 = User.objects.create_user(username2, password)
        second_vacancy.user = user2
        second_vacancy.employer = self.employer
        second_vacancy.title = "Welder MIG-MAG"
        second_vacancy.salary_min = 60000
        second_vacancy.save()

        saved_vacancies = Vacancy.objects.all()
        self.assertEqual(saved_vacancies.count(), 2)

        first_saved_vacancy = saved_vacancies[0]
        second_saved_vacancy = saved_vacancies[1]
        self.assertEqual(first_saved_vacancy.title, 'Welder TIG')
        self.assertEqual(second_saved_vacancy.title, 'Welder MIG-MAG')

class VacanciesListTest(TestCase):

    def setUp(self):
        user_test_data = {
            'email': 'foo@bar.com',
            'first_name': 'anatoly',
            'last_name': 'popov',
            'password': 'testpass'
            }
        region_test_data = {
            'name' : 'MO'
            }
        mo_region = Region.objects.create(**region_test_data)
        city_test_data = {
            'name': 'MOSCOW',
            'region': mo_region
            }
        moscow = City.objects.create(**city_test_data)
        employer_test_data = {
            'name': 'LUKOIL',
            'short_name': 'LUK',
            'inn': '123456789012',
            'city': moscow,
            'phone': '123',
            'email': 'test_email@test.com'
            }
        self.user = User.objects.create(**user_test_data)
        self.employer = Employer.objects.create(**employer_test_data)
        number_of_vacancies = 15
        for i in range(number_of_vacancies):
            Vacancy.objects.create(
                user=self.user,
                title="title", 
                salary_min=50000, 
                employer=self.employer)

    def test_list_url_resolves_to_list_view(self):
        found = resolve('/vacancies/list/')
        self.assertEqual(found.func, vacancies_list)

    def test_list_page_returns_correct_html(self):
        response = self.client.get('/vacancies/list/')
        self.assertTrue(response.status_code, '200')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Список вакансий</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'vacancies/list.html')

    def test_view_accessable_by_name(self):
        response = self.client.get(reverse('vacancies:list'))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_fiveteen_and_number_of_pages_is_two(self):
        paginator = Paginator(Vacancy.objects.all(), 10)
        self.assertEqual(paginator.count, 15)
        self.assertEqual(paginator.num_pages, 2)

class VacancyFormAddTest(TestCase):

    def setUp(self):
        self.user_test_data = {
            'email': 'foo@bar.com',
            'first_name': 'anatoly',
            'last_name': 'popov',
            'password': 'testpass'
            }
        self.user = User.objects.create(**self.user_test_data)
        self.level = Level.objects.create(name='I')

        self.vacancy_test_data = {
            'title': 'WELDER',
            'salary_min': '100',
            'salary_max': '200',
            'naks_att_level': [self.level.id],
            'short_description': 'WELDER NEEDED',
            'description': '<p>WELDER NEEDED</p>\r\n'
        }

    def test_load_form_correctly(self):
        response = self.client.get(reverse('vacancies:vacancy_create'))
        status_codes = (
            HTTPStatus.ACCEPTED,
            HTTPStatus.MOVED_PERMANENTLY,
            HTTPStatus.FOUND,
            HTTPStatus.SEE_OTHER,
            HTTPStatus.TEMPORARY_REDIRECT,
            HTTPStatus.PERMANENT_REDIRECT,
        )
        self.assertIn(response.status_code, status_codes)
        self.assertTemplateUsed('add-new-vacancy.html')

    def test_valid_data(self):
        form = VacancyForm(self.vacancy_test_data)
        self.assertTrue(form.is_valid())
    
    def test_missing_form_fields(self):
        incorrect_form_data = {}
        form = VacancyForm(incorrect_form_data)
        errors = form.errors.as_data()
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors['title'][0].code, 'required')
        self.assertEqual(errors['short_description'][0].code, 'required')
        self.assertEqual(errors['naks_att_level'][0].code, 'required')
    
    def test_passing_string_to_salary_fields(self):
        incorrect_salary = self.vacancy_test_data
        incorrect_salary['salary_min'] = 'one hundred thousands'
        incorrect_salary['salary_max'] = 'two hundred thousands'
        form = VacancyForm(self.vacancy_test_data)
        self.assertFalse(form.is_valid())

    def test_save_correct_form_to_database(self):
        response = self.client.get('/vacancies/new/')
        self.assertRedirects(response, '/users/login/?next=/vacancies/new/')
        self.client.force_login(self.user)
        self.client.post('/vacancies/new/', data=self.vacancy_test_data)
        vacancy = Vacancy.objects.first()
        self.assertEqual(vacancy.user, self.user)

class VacancyEditTest(TestCase):

    def setUp(self):
        mixer.cycle(1).blend(Level)
        self.levels = Level.objects.all()
        mixer.cycle(15).blend(Vacancy, naks_att_level__id=mixer.SELECT)
        self.vacancies = Vacancy.objects.all()
        self.vacancy = self.vacancies[random.randint(0, 14)]
        self.vacancy_data = self.vacancy.__dict__
        # vacancies = [repr(r) for r in Vacancy.objects.all()[:10]]
    
    def test_vacancies_are_in_database(self):
        self.assertEqual(len(self.vacancies), 15)

    def test_get_vacancy_by_id(self):
        vacancy = Vacancy.objects.get(id=self.vacancies[0].id)
        self.assertTrue(vacancy)
        self.assertTrue(isinstance(vacancy.title, str))
        self.assertTrue(isinstance(vacancy.salary_min, int))

    def test_get_vacancy_by_id(self):
        url = reverse('vacancies:vacancy_update', kwargs={'pk': self.vacancy.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('update-vacancy.html')
        self.assertTrue(isinstance(response.context['form'], VacancyForm))
    
    def test_vacancy_form_exist(self):
        url = reverse('vacancies:vacancy_update', kwargs={'pk': self.vacancy.pk})
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], VacancyForm))
        form = VacancyForm(data=self.vacancy_data)
        form.save(commit=False)
        form.user = 
        new_vacancy = form.save()
        self.assertTrue(form.is_valid())






