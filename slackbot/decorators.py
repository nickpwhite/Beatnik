import functools
import logging

from slackbot.views import SlackEvent

def slackevent(app_name_or_func, log_exceptions=True):
    def _slackevent(func, app_name=None):
        @functools.wraps(func)
        def wrapped(*args, **kw):
            payload = kw['slack_payload']
            if (payload.get('event')
                    and payload['event']['type'] == func.__name__
                    and app_name == kw['derived_app_name']):
                try:
                    return func(payload, *args, **kw)
                except:
                    if log_exceptions:
                        logging.exception('Error handling Slack Event "%s"',
                                          payload['event']['type'])
                    raise

        SlackEvent.connect(wrapped)
        return wrapped

    if callable(app_name_or_func):
        return _slackevent(app_name_or_func)

    return functools.partial(_slackevent, app_name=app_name_or_func)
