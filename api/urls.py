from django.urls import re_path

from api.views import Convert

urlpatterns = [
    re_path(r'^convert/?', Convert.as_view())
]
