from django.db.models import Model, EmailField, CharField, TextField

class Message(Model):
    from_address = EmailField("User inputted email address")
    subject = CharField("Email subject", max_length = 78)
    body = TextField("Email body")

    class Meta:
        unique_together = ('from_address', 'subject', 'body')
