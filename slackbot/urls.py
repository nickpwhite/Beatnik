from django.urls import re_path
from django_slack_events import SlackEventHandler
from slackbot.views import Authorize

urlpatterns = [
    re_path(r'^authorize/?', Authorize.as_view()),
    re_path(r'^events/?', SlackEventHandler.as_view()),
]
