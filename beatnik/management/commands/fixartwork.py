from beatnik.api_manager import ApiManager
from beatnik.models import Music
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Converts all entries with non-Spotify sourced artwork to use Spotify artwork'

    def handle(self, *args, **options):
        sql = "SELECT * FROM beatnik_music WHERE artwork NOT ILIKE '%%scdn%%'"
        bad_artwork = Music.objects.raw(sql)
        api_manager = ApiManager()

        for music in bad_artwork:
            spotify_artwork = api_manager.link_parser.get_spotify_artwork(music)
            if spotify_artwork is not None:
                music.artwork = spotify_artwork
                music.save()
