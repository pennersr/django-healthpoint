from django.urls import re_path

from healthpoint import views


urlpatterns = [re_path(r"^health/$", views.health, name="healthpoint_health")]
