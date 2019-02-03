from api_manager.ApiManager import ApiManager
from api_manager.LinkParser import LinkParser
from django.db.models import Manager, Model, CharField, IntegerField, URLField
from urllib import parse

class MusicManager(Manager):
    # convert :: Music -> Music
    def convert(self, music, link):
        api_manager = ApiManager()
        data = api_manager.link_converter.convert_link(link)

        music.music_type = 'A' if data['type'] == "album" else 'T'
        music.name = data['title']
        music.artist = data['artist']
        music.album = data.get('album', '')
        music.apple_url = data['links']['apple_link']
        music.gpm_url = data['links']['gpm_link']
        music.soundcloud_url = data['links']['soundcloud_link']
        music.spotify_url = data['links']['spotify_link']
        music.artwork = data['art']

        return music

    # get_or_create :: (6)Tuple -> Music
    def get_or_create(self, url):
        if LinkParser.apple_netloc in url.netloc:
            link = parse.urlunparse(url)
            music, new = super().get_or_create(apple_url=link)
        elif LinkParser.gpm_netloc in url.netloc:
            link = "{0}://music.google.com{1}".format(url.scheme, url.path)
            music, new = super().get_or_create(gpm_url=link)
        elif LinkParser.soundcloud_netloc in url.netloc:
            link = parse.urlunparse(url)
            music, new = super().get_or_create(soundcloud_url=link)
        elif LinkParser.spotify_netloc in url.netloc:
            link = parse.urlunparse(url)
            music, new = super().get_or_create(spotify_url=link)
        else:
            raise ValueError("{0} is not a supported url".format(url))

        if new:
            music = self.convert(music, link)
            music.save()

        return music

    # verify_url :: (6)Tuple -> Boolean
    def verify_url(self, url):
        return LinkParser.apple_netloc in url.netloc \
                or LinkParser.gpm_netloc in url.netloc \
                or LinkParser.soundcloud_netloc not in url.netloc \
                or LinkParser.spotify_netloc in url.netloc

class Music(Model):
    objects = MusicManager()

    music_type = CharField("Album or Track", max_length = 1, choices=(('A', 'Album'), ('T', 'Track')))
    name = CharField("Track Name", max_length = 200)
    artist = CharField("Artist Name", max_length = 200)
    album = CharField("Album Name", max_length = 200, blank = True)
    apple_url = URLField("Apple Music URL", null = True, unique = True)
    gpm_url = URLField("Google Play Music URL", null = True, unique = True)
    soundcloud_url = URLField("Soundcloud URL", null = True, unique = True)
    spotify_url = URLField("Spotify URL", null = True, unique = True)
    match_rating = IntegerField("Rating of the match", default = 0)
    artwork = URLField("Album art URL")

    def get_absolute_url(self):
        return "/music/{0}".format(self.id)
