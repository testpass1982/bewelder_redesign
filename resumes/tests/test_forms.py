from django.test import TestCase

from resumes.forms import ResumeForm


class ResumeFormTestCase(TestCase):
    def test_exclude_user_field(self):
        form = ResumeForm()
        self.assertNotIn('user', form.fields.keys())
