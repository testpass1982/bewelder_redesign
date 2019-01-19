from django.test import TestCase
from orgs.models import Employer, City, Region


class EmployerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_region = Region.objects.create(name='Region 1')
        city_1 = City.objects.create(name='City 1', region=test_region)
        city_2 = City.objects.create(name='City 2', region=test_region)

        employer_data = {
            'name': 'Employer1',
            'short_name': 'Emp. 1',
            'inn': '123456789012',
            'city': city_1,
            'phone': '123',
            'email': 'test@email.local',
        }
        Employer.objects.create(**employer_data)

        employer_data_2 = employer_data
        employer_data_2['name'] = 'Employer 2'
        employer_data_2['short_name'] = 'Emp. 2'
        Employer.objects.create(**employer_data_2)

        employer_data_3 = employer_data
        employer_data_3['city'] = city_2
        Employer.objects.create(**employer_data_3)

    def test_employers_creation(self):
        employer_1_city_1 = Employer.objects.get(name='Employer 1', city__name='City 1')
        employer_2_city_1 = Employer.objects.get(name='Employer 2', city__name='City 1')
        employer_1_city_2 = Employer.objects.get(name='Employer 1', city__name='City 2')

        self.assertEqual(employer_1_city_1.name, 'Employer 1')
        self.assertEqual(employer_2_city_1.name, 'Employer 2')
        self.assertEqual(employer_1_city_2.name, 'Employer 1')
        self.assertEqual(employer_1_city_1.city.name, 'City 1')
        self.assertEqual(employer_2_city_1.city.name, 'City 1')
        self.assertEqual(employer_1_city_2.city.name, 'City 2')
