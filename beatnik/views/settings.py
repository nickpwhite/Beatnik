from django.shortcuts import render
from django.views import View

class Settings(View):
    def get(self, request):
        context = {
            'redirect_to': request.session.get('redirect_to', 'none'),
            'tracking': request.session.get('tracking', 'off')
        }

        return render(request, 'settings.html', context)

    def post(self, request):
        context = {
            'redirect_to': request.POST.get('redirect_to'),
            'tracking': request.POST.get('tracking', 'off')
        }

        request.session['redirect_to'] = context['redirect_to']
        request.session['tracking'] = context['tracking']

        return render(request, 'settings.html', context)
