import base64

from django.conf import settings
from django.http import JsonResponse

from healthpoint.registry import get_health_checks


def _show_health_details(request):
    # Only staff members are allowed to see details...
    user = getattr(request, 'user', None)
    if user is not None and (user.is_staff or user.is_superuser):
        return True
    ba_username = getattr(settings, 'HEALTHPOINT_BASICAUTH_USERNAME', None)
    ba_password = getattr(settings, 'HEALTHPOINT_BASICAUTH_PASSWORD', None)
    authorization = request.META.get('HTTP_AUTHORIZATION')
    if ba_username and ba_password and authorization:
        method, _, auth = authorization.partition(' ')
        if method.lower() == 'basic':
            auth = base64.b64decode(auth.strip()).decode('utf8')
            username, _, password = auth.partition(':')
            return (username == ba_username and password == ba_password)
    return False


def health(request):
    tests = request.GET.getlist('test')
    data = {'success': {}, 'error': {}}
    status = 200
    for health_check in get_health_checks():
        func = '.'.join([
            health_check.__module__,
            health_check.__qualname__])
        if tests and func not in tests:
            continue
        success, detail = health_check()
        data['success' if success else 'error'][func] = detail
        if not success:
            status = 503
    # Only staff members are allowed to see details...
    if not _show_health_details(request):
        data = {}
    return JsonResponse(data, status=status)
