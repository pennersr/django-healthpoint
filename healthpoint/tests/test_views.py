from django.core.urlresolvers import reverse
from django.test import TestCase


class HealthTestCase(TestCase):

    def test_health(self):
        resp = self.client.get(reverse('healthpoint_health'))
        self.assertEqual(resp.status_code, 503)

    def test_health_failure(self):
        resp = self._test_func('healthpoint.tests.health.failure')
        self.assertEqual(resp.status_code, 503)

    def test_health_success(self):
        resp = self._test_func('healthpoint.tests.health.success')
        self.assertEqual(resp.status_code, 200)

    def _test_func(self, func):
        return self.client.get(reverse('healthpoint_health') + '?test=' + func)
