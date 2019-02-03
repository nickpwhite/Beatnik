from django.db.models import Model, BooleanField, CharField, TextField, IntegerField, URLField

class FormSubmit(Model):
    user_agent = TextField("Client's user agent", null = True)
    ip_address = CharField("Client's IP address", max_length = 45, null = True)
    referer = URLField("HTTP referer", null = True)
    query_string = TextField("Query string")
    query = TextField("The 'q' parameter in the query")

class MusicAccess(Model):
    user_agent = TextField("Client's user agent", null = True)
    ip_address = CharField("Client's IP address", max_length = 45, null = True)
    referer = URLField("HTTP referer", null = True)
    music_id = IntegerField("Id accessed")

class MusicClick(Model):
    APPLE = 'apple'
    GPM = 'gpm'
    SOUNDCLOUD = 'soundcloud'
    SPOTIFY = 'spotify'
    LINK_TYPE_CHOICES = [
        (APPLE, 'Apple Music'),
        (GPM, 'Google Play Music'),
        (SOUNDCLOUD, 'Soundcloud'),
        (SPOTIFY, 'Spotify')
    ]

    NETLOC_TO_TYPE = {
        'itunes.apple.com': APPLE,
        'music.google.com': GPM,
        'soundcloud.com': SOUNDCLOUD,
        'open.spotify.com': SPOTIFY
    }

    user_agent = TextField("Client's user agent", null = True)
    ip_address = CharField("Client's IP address", max_length = 45, null = True)
    referer = URLField("HTTP referer", null = True)
    link = URLField("The web address of the link clicked")
    link_type = CharField("Type of link", max_length = 10, choices = LINK_TYPE_CHOICES)
    redirect = BooleanField("Whether or not the redirect checkbox was checked", default = False)
