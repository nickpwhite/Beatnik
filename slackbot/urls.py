from django.urls import re_path
from slackbot.views import Authorize, SlackEventHandler

urlpatterns = [
    re_path(r'^authorize/?', Authorize.as_view()),
    re_path(r'^events/?', SlackEventHandler.as_view()),
]
