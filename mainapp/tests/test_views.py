from django.test import TestCase
from django.urls import reverse

from mixer.backend.django import mixer
from resumes.models import Resume


class HomePageViewTestCase(TestCase):
    def test_home_page(self):
        mixer.cycle(10).blend(Resume)

        resp = self.client.get(reverse('mainapp:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('resumes', resp.context)
        self.assertEqual(len(resp.context['resumes']), 5)

        self.assertIn('resumes_count', resp.context)
        self.assertEqual(resp.context['resumes_count'], 10)
