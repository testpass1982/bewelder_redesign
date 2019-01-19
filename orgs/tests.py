from django.test import TestCase
from django.urls import reverse
from orgs.models import Employer, City, Region


EMPLOYERS_PER_PAGE = 5


class EmployerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_region = Region.objects.create(name='Region 1')

        for city_num in range(3):
            city_ = City.objects.create(name='City {0}'.format(city_num), region=test_region)
            for emp_num in range(3):
                employer_data = {
                    'name': 'Employer {0}'.format(emp_num),
                    'inn': '123456789012',
                    'city': city_,
                    'phone': '123',
                    'email': 'test@email.local',
                }
                Employer.objects.create(**employer_data)

    def test_employers_creation(self):
        for city_num in range(3):
            city_name = 'City {0}'.format(city_num)
            for emp_num in range(3):
                emp_name = 'Employer {0}'.format(emp_num)
                emp_ = Employer.objects.get(name=emp_name, city__name=city_name)
                self.assertEqual(emp_.name, emp_name)
                self.assertEqual(emp_.city.name, city_name)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('orgs:list'))
        self.assertEqual(response.status_code, 200)
