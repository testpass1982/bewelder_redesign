from django.test import TestCase
from django.urls import reverse


class OrgsViewTest(TestCase):
    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('orgs:list'))
        self.assertEqual(response.status_code, 200)
