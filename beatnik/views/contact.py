from beatnik.models import Message
from django.db import IntegrityError
from django.shortcuts import render
from django.views import View

class Contact(View):
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
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

        try:
            Message.objects.create(
                from_address = from_address,
                subject = subject,
                body = body
            )
        except IntegrityError:
            return render(request, 'contact.html', { 'success': False, 'message': 'Already submitted' })

        return render(request, 'contact.html', { 'success': True })
