from django.conf import settings
from django.shortcuts import render
from django.views import View
from slackbot.models import Install

import slack


class Authorize(View):
    def get(self, request):
        auth_code = request.GET.get('code')

        client = slack.WebClient(token="")

        response = client.oauth_v2_access(
            client_id=settings.SLACK_CLIENT_ID,
            client_secret=settings.SLACK_CLIENT_SECRET,
            code=auth_code
        )

        install, created = Install.objects.get_or_create(
            team_id=response['team']['id'],
            defaults={
                'app_id': response['app_id'],
                'authed_user_id': response['authed_user']['id'],
                'scope': response['scope'],
                'access_token': response['access_token'],
                'bot_user_id': response['bot_user_id'],
                'team_name': response['team']['name'],
            }
        )

        context = {
            'install': install,
            'created': created
        }

        return render(request, 'authorize.html', context)
