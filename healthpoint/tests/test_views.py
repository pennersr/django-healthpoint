from django.core.urlresolvers import reverse
import base64
from django.test import TestCase, override_settings
from django.utils.http import urlencode


class HealthTestCase(TestCase):
    def test_health(self):
        resp = self.client.get(reverse("healthpoint_health"))
        self.assertEqual(resp.status_code, 503)
        self.assertEqual(resp.json(), {})

    def test_health_failure(self):
        resp = self._test_func("healthpoint.tests.health.failure")
        self.assertEqual(resp.status_code, 503)
        self.assertEqual(resp.json(), {})

    def test_health_success(self):
        resp = self._test_func("healthpoint.tests.health.success")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {})

    def test_unknown_health(self):
        resp = self._test_func("does.not.exist")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), {})

    def test_unknown_health_and_success(self):
        resp = self._test_func("does.not.exist", "healthpoint.tests.health.success")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), {})

    def test_unknown_health_and_failure(self):
        resp = self._test_func("does.not.exist", "healthpoint.tests.health.failure")
        self.assertEqual(resp.status_code, 503)
        self.assertEqual(resp.json(), {})

    @override_settings(
        HEALTHPOINT_BASICAUTH_USERNAME="john", HEALTHPOINT_BASICAUTH_PASSWORD="doe"
    )
    def test_health_with_basic_auth(self):
        headers = {
            "HTTP_AUTHORIZATION": "Basic "
            + base64.b64encode(b"john:doe").decode("ascii")
        }
        resp = self.client.get(reverse("healthpoint_health"), **headers)
        self.assertEqual(resp.status_code, 503)
        self.assertEqual(
            resp.json(),
            {
                "success": {
                    "healthpoint.tests.health.success": "This check always succeeds"
                },
                "error": {
                    "healthpoint.tests.health.failure": "This check always fails"
                },
            },
        )

    @override_settings(HEALTHPOINT_AUTH_REQUIRED=True)
    def test_health_with_auth_required(self):
        resp = self.client.get(reverse("healthpoint_health"))
        self.assertEqual(resp.status_code, 403)

    def _test_func(self, *func):
        params = urlencode({"test": func}, doseq=True)
        return self.client.get(reverse("healthpoint_health") + "?" + params)
