from django.test import TestCase
from django.test import Client
from django.urls import resolve
from django.http import HttpRequest
# from django.template.loader import render_to_string
from vacancies.views import list
# from mainapp.views import main
# Create your tests here.

# class SmokeTest(TestCase):

#     def test_bad_maths(self):
#         self.assertEqual(1+1, 3)

class VacanciesListTest(TestCase):

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
