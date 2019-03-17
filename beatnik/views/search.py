from beatnik.models.analytics import FormSubmit
from beatnik.models.music import Music
from django.shortcuts import redirect, render
from django.views import View
from urllib import parse

class Search(View):
    def get(self, request):
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
