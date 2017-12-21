import json

from beatnik.forms import LinkConverterForm
from beatnik.models import Music as MusicModel
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
            if LinkParser.apple_netloc in url.netloc:
                info = MusicModel.objects.filter(apple_url = parse.urlunparse(url))
            elif LinkParser.gpm_netloc in url.netloc:
                info = MusicModel.objects.filter(gpm_url = parse.urlunparse(url))
            elif LinkParser.soundcloud_netloc in url.netloc:
                info = MusicModel.objects.filter(soundcloud_url = parse.urlunparse(url))
            elif LinkParser.spotify_netloc in url.netloc:
                info = MusicModel.objects.filter(spotify_url = parse.urlunparse(url))
            else:
                return HttpResponse(status=404)

            if (len(info) == 0):
                linkConverter = LinkConverter()
                data = linkConverter.convert_link(link)
                print(data)
                info = Music(
                        music_type = data['type'],
                        name = data['title'],
                        artist = data['artist'],
                        album = data.get('album', ''),
                        apple_url = data['links']['apple_link'],
                        gpm_url = data['links']['gpm_link'],
                        soundcloud_url = data['links']['soundcloud_link'],
                        spotify_url = data['links']['spotify_link'],
                        artwork = data['art'])

            print(info)
            return JsonResponse(json.dumps(info.__dict__), safe=False)
        else:
            return HttpResponse()
