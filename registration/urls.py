from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'^preview/?$', views.preview, name='preview'),
    url(r'^status/?$', views.status, name='status'),
]
