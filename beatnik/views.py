import json

from beatnik.forms import LinkConverterForm
from beatnik.models import Music as MusicModel
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

class Music(View):
    def get(self, request):
        link = request.GET.get('q', '')
        if (link != ''):
            linkConverter = LinkConverter()
            info = linkConverter.convert_link(link)
            return render(request, 'beatnik/music.html', { 'info': info })
        else:
            return HttpResponse("Not found")

class Convert(View):
    def get(self, request):
        form = LinkConverterForm()
        return render(request, 'beatnik/linkConverter.html', { 'form': form, 'info': None })

    def post(self, request):
        form = LinkConverterForm(request.POST)
        info = None
        if (form.is_valid()):
            linkConverter = LinkConverter()
            info = linkConverter.convert_link(form.cleaned_data['link'])
        return render(request, 'beatnik/linkConverter.html', { 'form': form, 'info': info })

class MusicApi(View):
    def get(self, request):
        link = request.GET.get('q')
        if (link):
            url = parse.urlparse(link)
            link = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            if LinkParser.apple_netloc in url.netloc:
                info = MusicModel.objects.filter(apple_url = link)
            elif LinkParser.gpm_netloc in url.netloc:
                info = MusicModel.objects.filter(gpm_url = link)
                print(info)
            elif LinkParser.soundcloud_netloc in url.netloc:
                info = MusicModel.objects.filter(soundcloud_url = link)
            elif LinkParser.spotify_netloc in url.netloc:
                info = MusicModel.objects.filter(spotify_url = link)
            else:
                return HttpResponse(status=404)

            if (len(info) == 0):
                linkConverter = LinkConverter()
                data = linkConverter.convert_link(link)
                info = [MusicModel.objects.create(
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
