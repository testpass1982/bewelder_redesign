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
        user = mixer.blend(User)
        self.client.force_login(user)
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


class EmployerUpdateTestCase(TestCase):
    def setUp(self):
        self.user = mixer.blend(User)
        self.region_1 = Region.objects.create(name='Region 1')
        self.city_1 = City.objects.create(name='City 1', region=self.region_1)
        self.employer_data = {
            'name': 'Employer 1',
            'inn': '123456789012',
            'city': self.city_1,
            'phone': '123',
            'email': 'test@email.local',
            'user': self.user,
        }
        self.employer_1 = Employer.objects.create(**self.employer_data)
        self.url_update = reverse('orgs:update', kwargs={'pk': self.employer_1.id})

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
        # self.assertRedirects(
        #     response,
        #     reverse(
        #         'orgs:detail',
        #         args=[response.context['employer'].pk]
        #     )
        # )
        self.assertEqual(
            response.context['employer'].name,
            response.context['employer'].short_name,
        )
        self.assertEqual(
            response.context['employer'].name,
            self.employer_data['name']
        )


class EmployerDeleteTestCase(TestCase):
    def setUp(self):
        self.user = mixer.blend(User)
        self.region_1 = Region.objects.create(name='Region 1')
        self.city_1 = City.objects.create(name='City 1', region=self.region_1)
        self.employer_data = {
            'name': 'Employer 1',
            'inn': '123456789012',
            'city': self.city_1,
            'phone': '123',
            'email': 'test@email.local',
            'user': self.user
        }
        self.employer_1 = Employer.objects.create(**self.employer_data)
        self.url_delete = reverse('orgs:delete', kwargs={'pk': self.employer_1.id})

    def test_with_unauthorized(self):
        url_login = reverse('users:login')
        response = self.client.get(self.url_delete)
        self.assertRedirects(
            response,
            '{}?next={}'.format(url_login, self.url_delete)
        )
