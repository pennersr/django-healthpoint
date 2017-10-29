from django.core.urlresolvers import reverse
from django.test import TestCase


class HealthTestCase(TestCase):

    def test_health(self):
        resp = self.client.get(reverse('healthpoint_health'))
        self.assertEqual(resp.status_code, 500)
