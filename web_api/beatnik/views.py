from django.http import HttpResponse
from django.shortcuts import render
from link_converter.LinkConverter import LinkConverter
from .forms import LinkConverterForm

def index(request):
    if (request.method == "GET"):
        return render(request, 'beatnik/index.html')
    else:
        return HttpResponse()

def music(request):
    if (request.method == "GET"):
        link = request.GET.get('q', '')
        if (link != ''):
            linkConverter = LinkConverter()
            links = linkConverter.convert_link(link)
            return render(request, 'beatnik/music.html', { 'links': links })
        else:
            return HttpResponse("Not found")
    else:
        return HttpResponse()

def linkConverter(request):
    if (request.method == "POST"):
        form = LinkConverterForm(request.POST)
        if (form.is_valid()):
            linkConverter = LinkConverter()
            links = linkConverter.convert_link(form.cleaned_data['link'])
            print(links)
    else:
        form = LinkConverterForm()
        links = None

    return render(request, 'beatnik/linkConverter.html', { 'form': form, 'links': links })

