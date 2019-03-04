from django.test import TestCase

from orgs.forms import EmployerForm


class EmployerFormTestCase(TestCase):
    def test_exclude_user_field(self):
        form = EmployerForm()
        self.assertNotIn('user', form.fields.keys())
