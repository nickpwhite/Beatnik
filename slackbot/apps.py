from django.apps import AppConfig


class SlackbotConfig(AppConfig):
    name = 'slackbot'

    def ready(self):
        import slackbot.signals
