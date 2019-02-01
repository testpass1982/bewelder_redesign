import os

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from haystack.utils.loading import ConnectionHandler, UnifiedIndex
from haystack import connections
from mixer.backend.django import mixer
from resumes.models import Resume
from resumes.search_indexes import ResumeIndex

TEST_INDEX = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(settings.BASE_DIR, 'whoosh_test_index'),
    },
}


@override_settings(HAYSTACK_CONNECTIONS=TEST_INDEX)
class ResumeSearchTestCase(TestCase):
    def setUp(self):
        super().setUp()

        mixer.cycle(5).blend(Resume, position='сварщик')
        mixer.cycle(3).blend(Resume, position='инженер')

        self.old_unified_index = connections['default']._index
        self.ui = UnifiedIndex()
        self.resume_index = ResumeIndex()
        self.ui.build(indexes=[self.resume_index])

        backend = connections['default'].get_backend()
        backend.clear()
        backend.update(self.resume_index, Resume.objects.all())

    def tearDown(self):
        connections['default']._index = self.old_unified_index
        return super().tearDown()

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
