from django.conf.urls import include, re_path


urlpatterns = [
    re_path(r"^", include("healthpoint.urls")),
]
