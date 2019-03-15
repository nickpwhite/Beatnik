from beatnik.models.message import Message
from beatnik.models.music import Music
from beatnik.models.analytics import FormSubmit, MusicAccess
from django.db import IntegrityError
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

    if request.session.get('tracking', 'off') == 'on':
        MusicAccess.objects.create(
            user_agent = request.META.get('USER_AGENT'),
            ip_address = request.META.get('REMOTE_ADDR'),
            referer = request.META.get('HTTP_REFERER'),
            music_id = key
        )

    try:
        music = Music.objects.get(pk = key)
    except Music.DoesNotExist as exception:
        return redirect('/')

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

    if request.session.get('tracking', 'off') == 'on':
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

def settings(request):
    print(vars(request))
    if request.method == 'GET':
        return get_settings(request)
    elif request.method == 'POST':
        return post_settings(request)
    else:
        return HttpResponse(status = 405)

def get_settings(request):
    context = {
        'redirect_to': request.session.get('redirect_to', 'none'),
        'tracking': request.session.get('tracking', 'off')
    }

    return render(request, 'settings.html', context)

def post_settings(request):
    context = {
        'redirect_to': request.POST.get('redirect_to'),
        'tracking': request.POST.get('tracking', 'off')
    }

    request.session['redirect_to'] = context['redirect_to']
    request.session['tracking'] = context['tracking']

    return render(request, 'settings.html', context)

def contact(request):
    if request.method == 'GET':
        return get_contact(request)
    elif request.method == 'POST':
        return post_contact(request)
    else:
        return HttpResponse(status = 405)

def get_contact(request):
    return render(request, 'contact.html')

def post_contact(request):
    errors = {}
    from_address = request.POST['address']
    subject = request.POST['subject']
    body = request.POST['body']

    if subject.strip() == "":
        errors['email'] = 'Empty email address'
    if subject.strip() == "":
        errors['subject'] = 'Empty subject'
    if body.strip() == "":
        errors['body'] = 'Empty body'

    if errors:
        return render(request, 'contact.html', { 'errors': errors, 'success': false })
    else:
        try:
            Message.objects.create(
                from_address = from_address,
                subject = subject,
                body = body
            )
        except IntegrityError:
            return render(request, 'contact.html', { 'success': False, 'message': 'Already submitted' })

        return render(request, 'contact.html', { 'success': True })
