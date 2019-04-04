from django.urls import path, re_path

from beatnik.views import About, Contact, Index, Music, Rating, Search, Settings

urlpatterns = [
    re_path(r'^music/(?P<key>[0-9]+)/?', Music.as_view()),
    re_path(r'^search/?', Search.as_view()),
    re_path(r'^settings/?', Settings.as_view()),
    re_path(r'^contact/?', Contact.as_view()),
    re_path(r'^about/?', About.as_view()),
    re_path(r'^rating/?', Rating.as_view()),
    re_path(r'^(?P<page>[0-9]+)/?', Index.as_view()),
    re_path(r'^.*$', Index.as_view()),
]
