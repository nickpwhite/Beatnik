from beatnik.models.music import Music as MusicModel
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

class Music(View):
    def get(self, request, key):
        try:
            music = MusicModel.objects.get(pk = key)
        except MusicModel.DoesNotExist as exception:
            # return render(request, "404.html")
            raise Http404("Music does not exist")

        redirect_to = request.session.get('redirect_to')

        if redirect_to == "apple" and music.apple_url is not None:
            return redirect(music.apple_url)
        elif redirect_to == "soundcloud" and music.soundcloud_url is not None:
            return redirect(music.soundcloud_url)
        elif redirect_to == "spotify" and music.soundcloud_url is not None:
            return redirect(music.spotify_url)
        elif redirect_to == "tidal" and music.tidal_url is not None:
            return redirect(music.tidal_url)
        elif redirect_to == "ytm" and music.ytm_url is not None:
            return redirect(music.ytm_url)
        else:
            rated = request.session.get('rated.{0}'.format(key), False)
            context = {
                'music': music,
                'rated': rated
            }

            return render(request, 'music.html', context)
