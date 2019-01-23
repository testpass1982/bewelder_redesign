from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mixer.backend.django import mixer

from resumes.models import Resume

User = get_user_model()


class ResumeListViewTestCase(TestCase):
    def test_resume_list_pagination(self):
        mixer.cycle(15).blend(Resume)
        resumes = [repr(r) for r in Resume.objects.all()[:10]]
        url = reverse('resumes:resume_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context_data['is_paginated'])
        self.assertQuerysetEqual(resp.context.get('resumes'), resumes)


class ResumeDetailViewTestCase(TestCase):
    def test_resume_detail_view(self):
        resume = mixer.blend(Resume)
        url = reverse('resumes:resume_detail', kwargs={'pk': resume.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context.get('resume'), resume)
