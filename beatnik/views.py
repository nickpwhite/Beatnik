from beatnik.models.music import Music
from beatnik.models.analytics import FormSubmit, MusicAccess, MusicClick
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

    redirect_to = request.session.get('redirect_to')

    if redirect_to == "apple" and music.apple_url is not None:
        return redirect(music.apple_url)
    elif redirect_to == "gpm" and music.gpm_url is not None:
        return redirect(music.gpm_url)
    elif redirect_to == "soundcloud" and music.soundcloud_url is not None:
        return redirect(music.soundcloud_url)
    elif redirect_to == "spotify" and music.soundcloud_url is not None:
        return redirect(music.spotify_url)
    else:
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

def open(request):
    if request.method != 'POST':
        return HttpResponse(status = 405)

    link = request.POST.get('link')
    url = parse.urlparse(link)
    link_type = MusicClick.NETLOC_TO_TYPE[url.netloc]

    does_redirect = request.POST.get('redirect') == 'on'

    if does_redirect:
        request.session['redirect_to'] = link_type
    elif 'redirect_to' in request.session:
        del request.session['redirect_to']

    MusicClick.objects.create(
        user_agent = request.META.get('USER_AGENT'),
        ip_address = request.META.get('REMOTE_ADDR'),
        referer = request.META.get('HTTP_REFERER'),
        link = link,
        link_type = link_type,
        redirect = does_redirect
    )

    return redirect(link)
