from beatnik.forms import LinkConverterForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from link_converter.LinkConverter import LinkConverter

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
