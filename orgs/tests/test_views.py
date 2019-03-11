import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mixer.backend.django import mixer

from orgs.models import Employer, City, Region
from orgs.views import EMPLOYERS_PER_PAGE
from orgs.forms import EmployerForm

from vacancies.models import Vacancy


User = get_user_model()


class EmployerListTestCase(TestCase):
    def test_employer_list_pagination(self):
        mixer.cycle(EMPLOYERS_PER_PAGE + 1).blend(Employer)
        employers = [repr(e) for e in Employer.objects.all()[:EMPLOYERS_PER_PAGE]]
        url = reverse('orgs:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data['is_paginated'])
        self.assertQuerysetEqual(response.context.get('employers'), employers)


class EmployerDetailTestCase(TestCase):
    def test_employer_detail(self):
        employer = mixer.blend(Employer)
        url = reverse('orgs:detail', kwargs={'pk': employer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('employer'), employer)


class EmployerCreateTestCase(TestCase):
    url_create = reverse('orgs:create')

    def test_with_unauthorized(self):
        url_login = reverse('users:login')
        self.assertRedirects(
            self.client.get(self.url_create),
            '{}?next={}'.format(url_login, self.url_create)
        )

    def test_user_has_resume_redirects_to_update(self):
        user = mixer.blend(User)
        mixer.blend(Employer, user=user)
        self.client.force_login(user)
        response = self.client.get(self.url_create)
        self.assertRedirects(
            response,
            reverse('orgs:update')
        )

    def test_create_employer(self):
        user = mixer.blend(User)
        self.client.force_login(user)
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orgs/employer_form.html')
        self.assertIsInstance(response.context['form'], EmployerForm)

        city = mixer.blend(City)
        employer_data = {
            'name': 'Employer 1',
            'inn': '123456789012',
            'city': city.id,
            'phone': '123',
            'email': 'test@email.local',
        }
        response = self.client.post(self.url_create, data=employer_data, follow=True)
        self.assertRedirects(
            response,
            reverse(
                'orgs:detail',
                args=[response.context['employer'].pk]
            )
        )
        self.assertEqual(
            response.context['employer'].name,
            response.context['employer'].short_name,
        )


class EmployerUpdateTestCase(TestCase):
    def setUp(self):
        self.user = mixer.blend(User)
        self.city = mixer.blend(City)
        self.employer_data = {
            'name': 'Employer 1',
            'inn': '123456789012',
            'city': self.city,
            'phone': '123',
            'email': 'test@email.local',
            'user': self.user,
        }
        self.employer_1 = Employer.objects.create(**self.employer_data)
        self.url_update = reverse('orgs:update')

    def test_with_unauthorized(self):
        url_login = reverse('users:login')
        self.assertRedirects(
            self.client.get(self.url_update),
            '{}?next={}'.format(url_login, self.url_update)
        )

    def test_update_employer(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url_update)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orgs/employer_form.html')
        self.assertIsInstance(response.context['form'], EmployerForm)

        self.employer_data['name'] = 'Employer 1 Updated'
        response = self.client.post(self.url_update, data=self.employer_data, follow=True)
        self.assertEqual(
            response.context['employer'].name,
            response.context['employer'].short_name,
        )
        self.assertEqual(
            response.context['employer'].name,
            self.employer_data['name']
        )


class EmployerDeleteTestCase(TestCase):
    url_delete = reverse('orgs:delete')

    def test_with_unauthorized(self):
        url_login = reverse('users:login')
        response = self.client.get(self.url_delete)
        self.assertRedirects(
            response,
            '{}?next={}'.format(url_login, self.url_delete)
        )

    def test_get_confirmation_view(self):
        user = mixer.blend(User)
        mixer.blend(Employer, user=user)
        self.client.force_login(user)
        response = self.client.get(reverse('orgs:delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orgs/employer_confirm_delete.html')

    def test_post(self):
        user = mixer.blend(User)
        mixer.blend(Employer, user=user)
        self.assertEqual(Employer.objects.count(), 1)
        self.client.force_login(user)
        response = self.client.post(reverse('orgs:delete'))
        self.assertRedirects(response, reverse('mainapp:settings'))
        self.assertEqual(Employer.objects.count(), 0)
        user.refresh_from_db()
        self.assertFalse(user.is_employer)

    def test_delete_nonexistent_resume(self):
        user = mixer.blend(User)
        self.client.force_login(user)
        response = self.client.post(reverse('orgs:delete'))
        self.assertEqual(response.status_code, 404)


class VacancyInCityTestCase(TestCase):
    def setUp(self):
        self.city = mixer.blend(City)
        self.employer = mixer.blend(Employer, city=self.city)
        mixer.cycle(3).blend(City)
        mixer.cycle(2).blend(Vacancy, employer=self.employer)
        mixer.cycle(3).blend(Vacancy)

    def test_get_city_search_list(self):
        url = reverse('orgs:city_search_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        cities = json.loads(response.content)['cities']
        self.assertEqual(len(cities), 4)

        url = reverse('orgs:city_search_list', kwargs={'name': self.city.name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        cities = json.loads(response.content)['cities']
        self.assertEqual(len(cities), 1)
        self.assertEqual(cities[0]['name'], self.city.name)

    def test_get_city_vacancies_list(self):
        url = reverse('orgs:city_vacancies_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        vacancies = json.loads(response.content)['vacancies']
        self.assertEqual(len(vacancies), 5)

        url = reverse('orgs:city_vacancies_list', kwargs={'city_id': self.city.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        vacancies = json.loads(response.content)['vacancies']

        self.assertEqual(len(vacancies), 2)
        for vacancy in vacancies:
            self.assertEqual(vacancy['employer__city__name'], self.city.name)
