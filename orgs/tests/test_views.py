from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mixer.backend.django import mixer

from orgs.models import Employer, City, Region
from orgs.views import EMPLOYERS_PER_PAGE
from orgs.forms import EmployerForm


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

    def test_create_employer(self):
        username = 'foo@bar.com'
        password = 'geekbrains'
        user = User.objects.create_user(username, password)
        self.client.login(username=username, password=password)
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orgs/employer_form.html')
        self.assertIsInstance(response.context['form'], EmployerForm)

        region_1 = Region.objects.create(name='Region 1')
        city_1 = City.objects.create(name='City 1', region=region_1)
        employer_data = {
            'name': 'Employer 1',
            'inn': '123456789012',
            'city': city_1.id,
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
