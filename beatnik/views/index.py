import math

from beatnik.models import Music
from django.shortcuts import render
from django.views import View

class Index(View):
    PAGE_SIZE = 10
    current_page = 0

    def get(self, request, page = 0):
        page_count = math.ceil(Music.objects.count() / self.PAGE_SIZE)
        self.current_page = int(page)
        offset = request.GET.get('offset', None)

        if offset is not None:
            new_page = self.current_page + int(offset)
            if new_page < 0:
                new_page = 0
            elif new_page >= page_count:
                new_page = page_count - 1

            self.current_page = new_page

        start = self.current_page * self.PAGE_SIZE
        end = (self.current_page + 1) * self.PAGE_SIZE
        context = {
            'current_page': self.current_page,
            'latest_music': Music.objects.order_by('-id')[start:end],
            'page_range': range(page_count),
        }
        return render(request, 'index.html', context)
