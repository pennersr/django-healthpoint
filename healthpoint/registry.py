import importlib

from django.conf import settings


_checks = []
_initialized = False


def get_health_checks():
    global _initialized
    if not _initialized:
        for app in settings.INSTALLED_APPS:
            try:
                importlib.import_module('{}.health'.format(app))
            except ImportError:
                pass
    return _checks


def register_health_check(f):
    _checks.append(f)
