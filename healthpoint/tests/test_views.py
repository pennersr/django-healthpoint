from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import urlencode


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

    def test_unknown_health(self):
        resp = self._test_func('does.not.exist')
        self.assertEqual(resp.status_code, 404)

    def test_unknown_health_and_success(self):
        resp = self._test_func('does.not.exist', 'healthpoint.tests.health.success')
        self.assertEqual(resp.status_code, 404)

    def test_unknown_health_and_failure(self):
        resp = self._test_func('does.not.exist', 'healthpoint.tests.health.failure')
        self.assertEqual(resp.status_code, 503)

    def _test_func(self, *func):
        params = urlencode({'test': func}, doseq=True)
        return self.client.get(reverse('healthpoint_health') + '?' + params)
