==============================
Welcome to django-healthpoint!
==============================

.. image:: https://badge.fury.io/py/django-healthpoint.png
   :target: http://badge.fury.io/py/django-healthpoint

.. image:: https://travis-ci.org/pennersr/django-healthpoint.png
   :target: http://travis-ci.org/pennersr/django-healthpoint

.. image:: https://img.shields.io/pypi/v/django-healthpoint.svg
   :target: https://pypi.python.org/pypi/django-healthpoint

.. image:: https://coveralls.io/repos/pennersr/django-healthpoint/badge.png?branch=master
   :alt: Coverage Status
   :target: https://coveralls.io/r/pennersr/django-healthpoint

.. image:: https://pennersr.github.io/img/bitcoin-badge.svg
   :target: https://blockchain.info/address/1AJXuBMPHkaDCNX2rwAy34bGgs7hmrePEr

Framework for adding an endpoint for health checks to your project.

Source code
  http://github.com/pennersr/django-healthpoint


Quickstart
==========

Install the app::

    # settings.py
    INSTALLED_APPS = [
        ...
        'healthpoint'
    ]

    # If specified, this user is able to see the details for each
    # individual check in the endpoint.
    HEALTHPOINT_BASICAUTH_USERNAME = 'john'
    HEALTHPOINT_BASICAUTH_PASSWORD = 'doe'

    # urls.py
    urlpatterns = [
        ...
        url(r'^', include('healthpoint.urls')),
    ]

Add a module named ``health.py`` to any of your apps. For example::

    from datetime import timedelta

    from django.contrib.auth.models import User
    from django.utils import timezone

    from healthpoint.decorators import health_check


    @health_check
    def user_signup():
        last_user = User.objects.last()
        time_since_last_signup = timezone.now() - last_user.date_joined
        # Return True/False, throw an exception, or return a tuple with a
        # detail message.
        return (
            time_since_last_signup <= timedelta(days=1),
            "last signup was: {}".format(last_user.date_joined))


The health checks can be accessed via the ``/health/`` endpoint:

- It executes all health checks, and reports status 200 if all checks succeed, status 500 otherwise.

- If a staff user is logged in, the endpoint reports the result for each individual check::

    {
     "success": {},
     "error": {
       "myproject.myapp.health.user_signup": "Last signup was: 2017-10-29 08:45:51"
     }
    }

- To provide more detail on the result, the ``@health_check`` can return a tuple ``(success:bool, detail:str)``. The detail message will be listed in the result.
