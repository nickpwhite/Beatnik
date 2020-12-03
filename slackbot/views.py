from django.conf import settings
from django.dispatch import Signal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from slackbot.models import Install
from slackbot.slack_event_type import SlackEventType

import hashlib
import hmac
import json
import logging
import os
import slack
from time import time


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


SlackEvent = Signal(providing_args=['slack_payload', 'derived_app_name'])


class SlackEventHandler(View):
    # Explanation: https://stackoverflow.com/a/27315856
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kw):
        return super().dispatch(*args, **kw)

    def post(self, request):
        event_data = self.verify_request(request)

        # Echo the URL verification challenge code back to Slack
        if 'challenge' in event_data:
            return JsonResponse(event_data['challenge'], safe=False)

        # Parse the Event payload and send the signal
        if 'event' in event_data:
            event_type=event_data['event']['type']
            self.logger.info("Dispatching Slack event '%s'" % event_type)
            SlackEvent.send(SlackEventType[event_type.upper()],
                            slack_payload=event_data,
                            derived_app_name=self.guess_bot_name(request))
        else:
            event_type = event_data['type']
            self.logger.info("Dispatching Slack interaction '%s'" % event_type)
            SlackEvent.send(SlackInteractionType[event_type.upper()],
                            slack_payload=event_data,
                            derived_app_name=self.guess_bot_name(request))
        return HttpResponse()

    def parse_request(self, request):
        # Parse the request payload into JSON
        try:
            return json.loads(request.body.decode())
        except JSONDecodeError:
            ## this isn't an event; it's an interaction
            ## https://api.slack.com/interactivity/handling#payloads
            return json.loads(request.POST['payload'])

    def verify_request(self, request):
        ## Adapted for Django from
        ## https://github.com/TwoBitAlchemist/python-slack-events-api/blob/master/slackeventsapi/server.py#L92-L123
        ## Original comments with single # preserved

        # Each request comes with request timestamp and request signature
        # emit an error if the timestamp is out of range
        req_timestamp = request.headers.get('X-Slack-Request-Timestamp')
        if abs(time() - int(req_timestamp)) > 60 * 5:
            self.logger.error('Invalid request timestamp')
            raise DjangoSlackEventException('Invalid request timestamp')

        # Verify the request signature using the app's signing secret
        # emit an error if the signature can't be verified
        req_signature = request.headers.get('X-Slack-Signature')
        if not self.verify_signature(request, req_timestamp, req_signature):
            self.logger.error('Invalid request signature')
            raise DjangoSlackEventException('Invalid request signature')

        return self.parse_request(request)

    def verify_signature(self, request, timestamp, signature):
        ## Simplified and adapted Python 3 only use case from
        ## https://github.com/TwoBitAlchemist/python-slack-events-api/blob/master/slackeventsapi/server.py#L47-L83
        ## Original comments with single # preserved

        # Verify the request signature of the request sent from Slack
        # Generate a new hash using the app's signing secret and request data

        # Compare the generated hash and incoming request signature
        req = ('v0:%s:%s' % (timestamp, request.body.decode())).encode()
        request_hash = 'v0=' + hmac.new(
            self.signing_secret(request).encode(),
            req, hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(request_hash, signature)

    def guess_bot_name(self, request):
        probably_not_real_bot_names = ('slack', 'event', 'events')
        bot_name = request.GET.get('for')
        if not bot_name:
            bot_name = request.path.split('/')[1]

        if bot_name and bot_name not in probably_not_real_bot_names:
            return bot_name

    def signing_secret(self, request):
        bot_name = self.guess_bot_name(request)
        if bot_name:
            env_var = 'DJANGO_SLACK_EVENT_%s_SIGNING_SECRET' % bot_name.upper()
        else:
            env_var = 'DJANGO_SLACK_EVENT_SIGNING_SECRET'

        try:
            return os.environ[env_var]
        except KeyError:
            raise DjangoSlackEventConfigMissing(env_var)

    @property
    def logger(self):
        return logging.getLogger('console')
