from beatnik.models import FormSubmit, Music, MusicAccess
from django.http import HttpResponse
from django.shortcuts import render, redirect
from urllib import parse

def index(request):
    if request.method != 'GET':
        return HttpResponse(status = 405)

    return render(request, 'index.html')

def music(request, key):
    if request.method != 'GET':
        return HttpResponse(status = 405)

    MusicAccess.objects.create(
        user_agent = request.META.get('USER_AGENT'),
        ip_address = request.META.get('REMOTE_ADDR'),
        referer = request.META.get('HTTP_REFERER'),
        music_id = key
    )

    music = Music.objects.get(pk = key)
    context = {
        'music': music
    }

    return render(request, 'music.html', context)

def search(request):
    if request.method != 'GET':
        return HttpResponse(status = 405)

    link = request.GET.get('q')
    FormSubmit.objects.create(
        user_agent = request.META.get('USER_AGENT'),
        ip_address = request.META.get('REMOTE_ADDR'),
        referer = request.META.get('HTTP_REFERER'),
        query_string = request.META.get('QUERY_STRING'),
        query = link
    )

    if (link is None):
        return redirect('index')

    url = parse.urlparse(link)
    if (url.netloc == '' or not Music.objects.verify_url(url)):
        context = {
            'errors': ["That's not a valid URL"]
        }
        return render(request, 'errors.html', context)

    try:
        info = Music.objects.get_or_create(url)
    except ValueError:
        return HttpResponse(status = 400)

    return redirect(info)
