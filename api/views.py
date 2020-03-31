from api.models import Request
from beatnik.models.music import Music
from django.http import JsonResponse
from django.views import View
from urllib import parse

class Convert(View):
    def get(self, request):
        query = request.GET.get('q')

        Request.objects.create(
            user_agent = request.META.get('USER_AGENT'),
            ip_address = request.META.get('REMOTE_ADDR'),
            referer = request.META.get('HTTP_REFERER'),
            query_string = request.META.get('QUERY_STRING'),
            query = query,
            path = request.META.get('PATH_INFO')
        )

        if (query is None):
            return JsonResponse({ 'errors': ['No query provided'] })

        url = parse.urlparse(query)
        if (Music.objects.verify_url(url)):
            music_obj = Music.objects.get_or_create(url)
        else:
            return JsonResponse({ 'errors': ['Unable to parse provided URL'] })

        response_dict = {
            'errors': [],
            'id': music_obj.id,
            'type': 'album' if music_obj.music_type == 'A' else 'track',
            'album_art': music_obj.artwork,
            'title': music_obj.name,
            'artist': music_obj.artist,
            'apple': music_obj.apple_url,
            'gpm': music_obj.gpm_url,
            'soundcloud': music_obj.soundcloud_url,
            'spotify': music_obj.spotify_url,
            'tidal': music_obj.tidal_url
        }

        if music_obj.music_type == 'T':
            response_dict['album'] = music_obj.album

        return JsonResponse(response_dict)
