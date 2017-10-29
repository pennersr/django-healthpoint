from django.http import JsonResponse

from healthpoint.registry import get_health_checks


def health(request):
    data = {'success': {}, 'error': {}}
    status = 200
    for health_check in get_health_checks():
        success, detail = health_check()
        func = '.'.join([
            health_check.__module__,
            health_check.__qualname__])
        data['success' if success else 'error'][func] = detail
        if not success:
            status = 500
    # Only staff members are allowed to see details...
    user = getattr(request, 'user', None)
    if user is None or not user.is_staff or not user.is_superuser:
        data = {}
    return JsonResponse(data, status=status)
