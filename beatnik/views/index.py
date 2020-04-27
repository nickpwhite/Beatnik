import math

from beatnik.models import Music
from django.conf import settings
from django.shortcuts import render
from django.views import View

class Index(View):
    PAGE_SIZE = 10

    def get(self, request, page = 0):
        page_count = math.ceil(Music.objects.count() / self.PAGE_SIZE)
        current_page = int(page)
        last_page = page_count - 1

        start = current_page * self.PAGE_SIZE
        end = (current_page + 1) * self.PAGE_SIZE
        if current_page == 0:
            page_range = [current_page, current_page + 1, current_page + 2]
        elif current_page == last_page:
            page_range = [current_page - 2, current_page - 1, current_page]
        else:
            page_range = [current_page - 1, current_page, current_page + 1]

        context = {
            'current_page': current_page,
            'last_page': last_page,
            'latest_music': Music.objects.exclude(artwork='').order_by('-id')[start:end],
            'page_range': page_range,
            'scopes': settings.SLACK_SCOPES,
        }
        return render(request, 'index.html', context)
