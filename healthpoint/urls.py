from django.conf.urls import url

from healthpoint import views


urlpatterns = [
    url(r'^health/$', views.health, name='healthpoint_health')
]
