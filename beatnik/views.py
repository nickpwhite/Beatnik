import json

from beatnik.forms import LinkConverterForm
from beatnik.models import Music
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from link_converter.LinkConverter import LinkConverter
from link_converter.LinkParser import LinkParser
from urllib import parse

class Index(View):
    def get(self, request):
        return render(request, 'beatnik/index.html')

class MusicApi(View):
    def get(self, request):
        link = request.GET.get('q')
        if (link):
            url = parse.urlparse(link)
            link = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            if LinkParser.apple_netloc in url.netloc:
                info = Music.objects.filter(apple_url = link)
            elif LinkParser.gpm_netloc in url.netloc:
                info = Music.objects.filter(gpm_url = link)
            elif LinkParser.soundcloud_netloc in url.netloc:
                info = Music.objects.filter(soundcloud_url = link)
            elif LinkParser.spotify_netloc in url.netloc:
                info = Music.objects.filter(spotify_url = link)
            else:
                return HttpResponse(status=404)

            if (len(info) == 0):
                linkConverter = LinkConverter()
                data = linkConverter.convert_link(link)
                info = [Music.objects.create(
                        music_type = 'A' if data['type'] == "album" else 'T',
                        name = data['title'],
                        artist = data['artist'],
                        album = data.get('album', ''),
                        apple_url = data['links']['apple_link'],
                        gpm_url = data['links']['gpm_link'],
                        soundcloud_url = data['links']['soundcloud_link'],
                        spotify_url = data['links']['spotify_link'],
                        artwork = data['art'])]

            return JsonResponse(serializers.serialize('json', info), safe=False)
        else:
            return HttpResponse(status=400)
