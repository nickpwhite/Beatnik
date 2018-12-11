import json
import os

from beatnik.models import Music as M
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from api_manager.ApiManager import ApiManager
from api_manager.LinkParser import LinkParser
from urllib import parse

class Index(View):
    def get(self, request):
        context = {
            'chrome_ext_url': "https://chrome.google.com/webstore/detail/beatnik/imhhnehiopfkoogocbgihgepdkedbcfi?hl=en-US",
            'firefox_ext_url': "https://addons.mozilla.org/en-US/firefox/addon/beatnik-app/"
        }
        return render(request, 'index.html', context)

class Music(View):
    def get(self, request):
        link = request.GET.get('q')
        url = parse.urlparse(link)
        if (url.netloc == '' or not M.objects.verify_url(url)):
            # TODO: return form back with error
            return HttpResponse(status=400)

        try:
            info = M.objects.get_or_create(url)
        except ValueError:
            return HttpResponse(status=400)

        context = {
            'music': info,
            'query': link
        }

        return render(request, 'music.html', context)

class MusicApi(View):
    def get(self, request):
        link = request.GET.get('q')
        url = parse.urlparse(link)
        if (url.netloc == '' or not M.objects.verify_url(url)):
            return HttpResponse(status=400)

        try:
            info = M.objects.get_or_create(url)
        except ValueError:
            return HttpResponse(status=400)

        json_response = json.loads(serializers.serialize('json', info))
        return JsonResponse(json_response, safe=False)
