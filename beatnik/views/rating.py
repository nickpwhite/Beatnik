from beatnik.models import Music
from django.shortcuts import redirect
from django.views import View

class Rating(View):
    def post(self, request):
        music_id = request.POST.get('music_id')
        session_key = 'rated.{0}'.format(music_id)

        if request.session.get(session_key, False):
            return redirect('/music/{0}'.format(music_id))

        music = Music.objects.get(pk = music_id)
        rating = int(request.POST.get('rating'))

        music.match_rating += rating
        music.save()
        request.session[session_key] = True

        return redirect('/music/{0}'.format(music_id))
