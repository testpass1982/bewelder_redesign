from django.test import TestCase
from django.test import Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from vacancies.views import list
from vacancies.models import Vacancy
from django.core.paginator import Paginator
from orgs.models import Employer
# Create your tests here.

# class SmokeTest(TestCase):

#     def test_bad_maths(self):
#         self.assertEqual(1+1, 3)

class VacancyModelTest(TestCase):

    def test_saving_and_retrieving_vacancies(self):
        employer = Employer()
        employer.name = 'LUKOIL'
        employer.save()
        first_vacancy = Vacancy()
        first_vacancy.title = 'Welder TIG'
        first_vacancy.salary_min = 50000 
        first_vacancy.employer = employer
        first_vacancy.save()

        second_vacancy = Vacancy()
        second_vacancy.title = "Welder MIG-MAG"
        second_vacancy.salary_min = 60000
        second_vacancy.employer = employer
        second_vacancy.save()

        saved_vacancies = Vacancy.objects.all()
        self.assertEqual(saved_vacancies.count(), 2)

        first_saved_vacancy = saved_vacancies[0]
        second_saved_vacancy = saved_vacancies[1]
        self.assertEqual(first_saved_vacancy.title, 'Welder TIG')
        self.assertEqual(second_saved_vacancy.title, 'Welder MIG-MAG')

class VacanciesListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_vacancies = 15
        test_employer = Employer.objects.create(name="Test_Employer_Title")
        for i in range(number_of_vacancies):
            Vacancy.objects.create(title="title", salary_min=50000, employer=test_employer)

    def test_list_url_resolves_to_list_view(self):
        found = resolve('/vacancies/list')
        self.assertEqual(found.func, list)

    def test_list_page_returns_correct_html(self):
        response = self.client.get('/vacancies/list')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n<html lang="en">'))
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