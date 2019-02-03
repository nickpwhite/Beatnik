from django.urls import path, re_path

from beatnik import views

urlpatterns = [
    re_path(r'^music/(?P<key>[0-9]+)/?', views.music),
    re_path(r'^open/?', views.open),
    re_path(r'^search/?', views.search),
    re_path(r'^.*$', views.index),
]
