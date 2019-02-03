import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from haystack import connections
from haystack.utils.loading import ConnectionHandler, UnifiedIndex
from mixer.backend.django import mixer
from resumes.models import Resume
from resumes.search_indexes import ResumeIndex
from users.models import User

TEST_INDEX = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'STORAGE': 'ram',
    },
}


@override_settings(HAYSTACK_CONNECTIONS=TEST_INDEX)
class ResumeSearchTestCase(TestCase):
    def setUp(self):
        mixer.cycle(5).blend(Resume, position='сварщик')
        mixer.cycle(3).blend(Resume, position='инженер')

        connections.reload('default')
        call_command('rebuild_index', interactive=False, verbosity=0)
        super().setUp()

    def test_search_view(self):
        resp = self.client.get(reverse('haystack_search'))
        self.assertEqual(resp.status_code, 200)

    def test_search_query(self):
        resp = self.client.get(reverse('haystack_search'), {'q': 'сварщик'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context[-1]['page'].object_list), 5)
        self.assertEqual(resp.context[-1]['page'].object_list[0].content_type(), 'resumes.resume')

        resp = self.client.get(reverse('haystack_search'), {'q': 'инженер'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context[-1]['page'].object_list), 3)
        self.assertEqual(resp.context[-1]['page'].object_list[0].content_type(), 'resumes.resume')

        resp = self.client.get(reverse('haystack_search'), {'q': 'директор'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context[-1]['page'].object_list), 0)
