from django.test import TestCase
from django.test import Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from vacancies.views import vacancies_list, vacancy_details
from vacancies.models import Vacancy, Level
from django.core.paginator import Paginator
from orgs.models import Employer, City, Region
from users.models import User
from http import HTTPStatus
from vacancies.forms import VacancyForm
from django.shortcuts import get_object_or_404
from mixer.backend.django import mixer
from model_mommy import mommy
from django.forms.models import model_to_dict
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

class TestVacancyUpdateForm(TestCase):
    def setUp(self):
        user_test_data = {
            'email': 'foo@bar.com',
            'first_name': 'anatoly',
            'last_name': 'popov',
            'password': 'testpass'
            }
        another_user_test_data = {
            'email': 'barbar@foo.com',
            'first_name': 'igor',
            'last_name': 'ivanov',
            'password': 'igor_ivanov'
            }
        self.user = User.objects.create(**user_test_data)
        self.another_user = User.objects.create(**another_user_test_data)
        self.levels = mommy.make(Level, _quantity=3)
        self.vacancies = mommy.make(Vacancy, _quantity=10, 
                                    make_m2m=True, 
                                    user=self.user,
                                    salary_min=300)
        self.level1 = Level.objects.create(name='I')
        for vacancy in self.vacancies:
            vacancy.naks_att_level.add(self.level1)

        self.vacancy = self.vacancies[random.randint(0, 9)]
    
    def test_vacancy_created(self):
        vacancies = self.vacancies
        self.assertEqual(len(vacancies), 10)
        vacancies[0].naks_att_level.add(self.level1)
        self.assertTrue(self.level1 in vacancies[0].naks_att_level.all())
    
    def test_vacancy_update_form_reachable_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('vacancies:vacancy_update', kwargs={'pk': self.vacancy.id}))
        self.assertTrue(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], VacancyForm))
        self.assertTrue(response.context['form']['title'].value()==self.vacancy.title)

    def test_vacancy_udpate_form_can_save_data(self):
        #Авторизуемся
        self.client.force_login(self.user)
        #Получаем ссылку для тестовых данных
        update_url = reverse('vacancies:vacancy_update', kwargs={'pk': self.vacancy.id})
        #Переходим по ссылке
        response = self.client.get(update_url)
        #Берем из формы данные
        form = response.context['form']
        data = form.initial
        #Меняем данные
        data['title'] = 'changed_title'
        data['salary_max'] = 400
        data['naks_att_level'] = self.level1.id
        #Делаем пост с измененными данными
        response = self.client.post(update_url, data)
        #Проверяем редирект после отправки данных
        self.assertRedirects(response, reverse('mainapp:settings'))
        #Еще раз заходим по ссылке
        response = self.client.get(update_url)
        #Проверяем, что измененные данные в форме
        self.assertEqual(response.context['form'].initial['title'], 'changed_title')
        self.assertEqual(response.context['form'].initial['salary_max'], 400)
        self.assertTrue(self.level1 in response.context['form'].initial['naks_att_level'])

    def test_user_cant_update_another_user_vacancies(self):
        self.client.force_login(self.user)
        user_vacancy = mommy.make(Vacancy, _quantity=1, 
                                  make_m2m=True,
                                  user=self.user,
                                  salary_min=500)
        self.client.logout()
        self.client.force_login(self.another_user)
        update_url = reverse('vacancies:vacancy_update', kwargs={'pk': user_vacancy[0].pk})
        response = self.client.post(update_url)
        self.assertTrue(response.status_code, 404)

class TestVacancyDelete(TestCase):
    def setUp(self):
        user_test_data = {
            'email': 'foo@bar.com',
            'first_name': 'anatoly',
            'last_name': 'popov',
            'password': 'testpass'
            }
        another_user_test_data = {
            'email': 'barbar@foo.com',
            'first_name': 'victor',
            'last_name': 'ivanov',
            'password': 'victor_ivanov'
            }
        self.user = User.objects.create(**user_test_data)
        self.another_user = User.objects.create(**another_user_test_data)
        self.levels = mommy.make(Level, _quantity=3)
        self.vacancies = mommy.make(Vacancy, _quantity=10, 
                                    make_m2m=True, 
                                    user=self.user,
                                    salary_min=300)
        self.level1 = Level.objects.create(name='I')
        for vacancy in self.vacancies:
            vacancy.naks_att_level.add(self.level1)
        random_choice = random.randint(0, 9)
        self.vacancy = self.vacancies[random_choice]

    def test_vacancy_created(self):
        self.assertTrue(len(self.vacancies), 10)
        self.assertTrue(self.level1 in self.vacancies[0].naks_att_level.all())
    
    def test_vacancy_can_be_deleted(self):
        self.client.force_login(self.user)
        url = reverse('vacancies:vacancy_delete', kwargs={'pk': self.vacancy.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'vacancies/vacancy_confirm_delete.html')
        response = self.client.post(url, data={'Confirm': 'Yes'})
        self.assertRedirects(response, reverse('mainapp:settings'))
        self.user.refresh_from_db()
        self.assertTrue(Vacancy.objects.filter(pk=self.vacancy.pk).count()==0)
    
    def test_nonexistent_vacancy_cant_be_deleted(self):
        self.client.force_login(self.user)
        url = reverse('vacancies:vacancy_delete', kwargs={'pk': 1000})
        response = self.client.post(url, data={'Confirm': 'YES'})
        self.assertEqual(response.status_code, 404)

    def test_not_authenticated_user_cant_delete_vacancy(self):
        url = reverse('vacancies:vacancy_delete', kwargs={'pk': self.vacancy.pk})
        response = self.client.post(url, data={'Confirm': 'YES'})
        self.assertRedirects(response, '/users/login/?next=/vacancies/delete/{}'.format(self.vacancy.pk))
    
    def test_user_cant_delete_other_users_vacancies(self):
        self.client.force_login(self.user)
        vacancy_user1 = mommy.make(Vacancy, _quantity=1, 
                                    make_m2m=True, 
                                    user=self.user,
                                    salary_min=300)
        self.client.logout()
        self.client.login(email=self.another_user.email, password=self.another_user.password)
        url = reverse('vacancies:vacancy_delete', kwargs={'pk': vacancy_user1[0].pk})
        response = self.client.post(url, data={'Confirm': 'YES'})
        self.assertTrue(response.status_code, 404)

class TestVacancyDetails(TestCase):
    def setUp(self):
        user_test_data = {
            'email': 'foo@bar.com',
            'first_name': 'anatoly',
            'last_name': 'popov',
            'password': 'testpass'
            }
        self.user = User.objects.create(**user_test_data)
        self.vacancies = mixer.cycle(10).blend(Vacancy, user=self.user)

    def test_details_url_resolves_to_details_view(self):
        for vacancy in self.vacancies:
            found = resolve('/vacancies/details/{}'.format(vacancy.pk))
            self.assertEqual(found.func, vacancy_details)

    def test_vacancy_details_reachable_by_pk(self):
        for vacancy in self.vacancies:
            url = reverse('vacancies:vacancy_details', kwargs={'pk': vacancy.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_vacancy_details_contains_related_vacancies(self):
        for vacancy in self.vacancies:
            url = reverse('vacancies:vacancy_details', kwargs={'pk': vacancy.pk})
            response = self.client.get(url)
            self.assertTrue(len(response.context['related_vacancies'])==3)

    def test_related_vacancies_reachable_by_pk(self):
        vacancy = self.vacancies[random.randint(0, len(self.vacancies))]
        url = reverse('vacancies:vacancy_details', kwargs={'pk': vacancy.pk})
        response = self.client.get(url)
        for vacancy in response.context['related_vacancies']:
            url = reverse('vacancies:vacancy_details', kwargs={'pk': vacancy.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            

