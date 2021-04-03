from django.shortcuts import render
from django.views import View

class Settings(View):
    def get(self, request):
        redirect_to = request.sesion.get('redirect_to', 'none')
        if redirect_to == 'gpm':
            redirect_to = 'none'

        context = {
            'redirect_to': redirect_to,
        }

        return render(request, 'settings.html', context)

    def post(self, request):
        context = {
            'redirect_to': request.POST.get('redirect_to'),
        }

        request.session['redirect_to'] = context['redirect_to']

        return render(request, 'settings.html', context)
