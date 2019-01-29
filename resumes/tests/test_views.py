from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mixer.backend.django import mixer

from resumes.models import Resume
from resumes.forms import ResumeForm

User = get_user_model()


class ResumeListTestCase(TestCase):
    def test_resume_list_pagination(self):
        mixer.cycle(15).blend(Resume)
        resumes = [repr(r) for r in Resume.objects.all()[:10]]
        url = reverse('resumes:resume_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context_data['is_paginated'])
        self.assertQuerysetEqual(resp.context.get('resumes'), resumes)


class ResumeDetailTestCase(TestCase):
    def test_resume_detail_view(self):
        resume = mixer.blend(Resume)
        url = reverse('resumes:resume_detail', kwargs={'pk': resume.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context.get('resume'), resume)


class ResumeDeleteTestCase(TestCase):
    def test_with_unauthorized(self):
        resp = self.client.get(reverse('resumes:resume_delete'))
        self.assertRedirects(
            resp,
            '{}?next={}'.format(reverse('users:login'), reverse('resumes:resume_delete'))
        )

    def test_get_confirmation_view(self):
        user = mixer.blend(User)
        resume = mixer.blend(Resume, user=user)
        self.client.force_login(user)

        resp = self.client.get(reverse('resumes:resume_delete'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'resumes/resume_confirm_delete.html')

    def test_post(self):
        user = mixer.blend(User)
        resume = mixer.blend(Resume, user=user)
        self.assertEqual(Resume.objects.count(), 1)

        self.client.force_login(user)

        resp = self.client.post(reverse('resumes:resume_delete'))
        self.assertRedirects(resp, reverse('mainapp:settings'))
        self.assertEqual(Resume.objects.count(), 0)
        user.refresh_from_db()
        self.assertFalse(user.is_seeker)

    def test_delete_nonexistent_resume(self):
        user = User.objects.create_user('foo@bar.com', 'password')
        self.client.force_login(user)
        resp = self.client.post(reverse('resumes:resume_delete'))
        self.assertEqual(resp.status_code, 404)


class ResumeCreateTestCase(TestCase):
    url_name = 'resumes:resume_create'

    def test_with_unauthorized(self):
        resp = self.client.get(reverse(self.url_name))
        self.assertRedirects(
            resp,
            '{}?next={}'.format(reverse('users:login'), reverse(self.url_name))
        )

    def test_user_has_resume_redirects_to_update(self):
        username = 'foo@bar.com'
        password = 'geekbrains'
        user = User.objects.create_user(username, password)
        resume = mixer.blend(Resume, user=user)
        self.client.login(username=username, password=password)
        resp = self.client.get(reverse(self.url_name))
        self.assertRedirects(
            resp,
            reverse('resumes:resume_update')
        )

    def test_create_resume(self):
        username = 'foo@bar.com'
        password = 'geekbrains'
        user = User.objects.create_user(username, password)
        self.client.login(username=username, password=password)
        resp = self.client.get(reverse(self.url_name))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'resumes/resume_form.html')
        self.assertFalse(hasattr(user, 'resume'))
        self.assertIsInstance(resp.context['form'], ResumeForm)

        data = {
            'position': 'welder',
            'salary_min': 10000,
        }
        resp = self.client.post(reverse(self.url_name), data=data, follow=True)
        self.assertRedirects(resp, reverse('resumes:resume_detail', args=[resp.context['resume'].pk]))
        user.refresh_from_db()
        self.assertTrue(hasattr(user, 'resume'))
        self.assertTrue(resp.context['resume'], user.resume)
