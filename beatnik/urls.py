from django.urls import path, re_path
from django.views.defaults import page_not_found

from beatnik.views import About, Index, Music, Rating, Search, Settings

def custom_page_not_found(request):
    return page_not_found(request, None)

urlpatterns = [
    re_path(r'^404/$', custom_page_not_found),
    re_path(r'^music/(?P<key>[0-9]+)/?', Music.as_view()),
    re_path(r'^search/?', Search.as_view()),
    re_path(r'^settings/?', Settings.as_view()),
    re_path(r'^about/?', About.as_view()),
    re_path(r'^rating/?', Rating.as_view()),
    re_path(r'^(?P<page>[0-9]+)/?', Index.as_view()),
    re_path(r'^.*$', Index.as_view()),
]
