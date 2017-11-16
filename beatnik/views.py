from django.http import HttpResponse
from django.shortcuts import render
from link_converter.LinkConverter import LinkConverter
from .forms import LinkConverterForm

def index(request):
    return render(request, 'beatnik/index.html')

def songs(request):
    link = request.GET.get('q', '')
    if (link != ''):
        linkConverter = LinkConverter()
        return HttpResponse(linkConverter.convert_link(link))
    return HttpResponse('')

def linkConverter(request):
    if (request.method == "POST"):
        form = LinkConverterForm(request.POST)
        if (form.is_valid()):
            linkConverter = LinkConverter()
            print(form.cleaned_data)
            links = linkConverter.convert_link(form.cleaned_data['link'])
    else:
        form = LinkConverterForm()
        links = None

    return render(request, 'beatnik/linkConverter.html', { 'form': form, 'links': links })
