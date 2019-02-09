from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from haystack import connections
from mixer.backend.django import mixer

from resumes.models import Resume
from search.forms import SearchForm


class ResumeSearchTestCase(TestCase):
    search_url = reverse('search:search')

    def setUp(self):
        mixer.cycle(5).blend(Resume, position='сварщик')
        mixer.cycle(3).blend(Resume, position='инженер')

        connections.reload('default')
        call_command('rebuild_index', interactive=False, verbosity=0)
        super().setUp()

    def test_search_view(self):
        resp = self.client.get(self.search_url)
        self.assertEqual(resp.status_code, 200)

    def test_search_query(self):
        resp = self.client.get(self.search_url, {'q': 'сварщик'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 5)
        self.assertEqual(resp.context['page'].object_list[0].content_type(), 'resumes.resume')

        resp = self.client.get(self.search_url, {'q': 'инженер'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 3)
        self.assertEqual(resp.context['page'].object_list[0].content_type(), 'resumes.resume')

        resp = self.client.get(self.search_url, {'q': 'директор'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 0)

    def test_realtime_update_search_index(self):
        position = 'рыбак'
        resp = self.client.get(self.search_url, {'q': position})
        old_obj_count = len(resp.context['page'].object_list)

        mixer.blend(Resume, position=position)

        resp = self.client.get(self.search_url, {'q': position})
        new_obj_count = len(resp.context['page'].object_list)
        self.assertEqual(new_obj_count, old_obj_count + 1)

    def test_search_only_resumes(self):
        resp = self.client.get(self.search_url, {'q': 'инженер', 'models': 'resumes.resume'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 3)
        self.assertEqual(resp.context['page'].object_list[0].content_type(), 'resumes.resume')

    def test_search_complex_query(self):
        queries = [
            'сварщик, москва',
            'сварщики, москва',
            'москва, сварщик',
            'москва, сварщики',
            'сварщик в москве',
            'сварщики по Москве',
            'сварщики из москвы',
        ]

        mixer.cycle(3).blend(Resume, position='сварщик', city='Москва')

        for query in queries:
            with self.subTest(q=query):
                resp = self.client.get(self.search_url, {'q': query})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(len(resp.context['page'].object_list), 3)
                self.assertEqual(resp.context['page'].object_list[0].content_type(), 'resumes.resume')

    def test_prepare_query(self):
        queries = [
            'сварщики по Москве',
            'сварщики из москвы',
            'сварщики, москва'
        ]
        expect = 'сварщик москв'

        for query in queries:
            with self.subTest(query_string=query):
                result = SearchForm().prepare_query(query)
                self.assertEqual(result, expect)
