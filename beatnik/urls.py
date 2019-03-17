from django.urls import path, re_path

from beatnik import views

urlpatterns = [
    re_path(r'^music/(?P<key>[0-9]+)/?', views.music),
    re_path(r'^search/?', views.search),
    re_path(r'^settings/?', views.settings),
    re_path(r'^contact/?', views.contact),
    re_path(r'^rating/?', views.rating),
    re_path(r'^.*$', views.index),
]
