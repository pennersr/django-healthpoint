import base64

from django.conf import settings
from django.http import JsonResponse
from healthpoint.registry import get_health_checks


def _is_authenticated_request(request):
    # Superusers and staff members are always correctly authenticated.
    user = getattr(request, "user", None)
    if user is not None and (user.is_staff or user.is_superuser):
        return True
    # Requests with basic authentication credentials are only
    # authenticated when they match the settings.
    ba_username = getattr(settings, "HEALTHPOINT_BASICAUTH_USERNAME", None)
    ba_password = getattr(settings, "HEALTHPOINT_BASICAUTH_PASSWORD", None)
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if ba_username and ba_password and authorization:
        method, _, auth = authorization.partition(" ")
        if method.lower() == "basic":
            auth = base64.b64decode(auth.strip()).decode("utf8")
            username, _, password = auth.partition(":")
            return username == ba_username and password == ba_password
    return False


def health(request):
    tests = set(request.GET.getlist("test"))
    tests_left = set(tests)
    data = {"success": {}, "error": {}}
    status = 200

    is_authenticated_request = _is_authenticated_request(request)
    authentication_required = getattr(settings, "HEALTHPOINT_AUTH_REQUIRED", False)

    if authentication_required and not is_authenticated_request:
        # The settings require a succesfully authenticated request
        # Abort the health checks if this is not the case...
        status = 403
        data = {}
    else:
        # Perform the actual health checks if the authentication is successful
        # or not required.
        for health_check in get_health_checks():
            func = ".".join([health_check.__module__, health_check.__qualname__])
            if tests and func not in tests:
                continue
            tests_left.discard(func)
            success, detail = health_check()
            data["success" if success else "error"][func] = detail
            if not success:
                status = 503
        if tests_left:
            if status == 200:
                status = 404
            for test in tests_left:
                data["error"][test] = "Unknown health check"

        # Only successfully authenticated requests are allowed to see the
        # full details of the results.
        if not is_authenticated_request:
            data = {}

    # Return the response
    return JsonResponse(data, status=status)
