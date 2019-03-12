from django.db.models import Model, BooleanField, CharField, TextField, IntegerField, URLField

class FormSubmit(Model):
    user_agent = TextField("Client's user agent", null = True)
    ip_address = CharField("Client's IP address", max_length = 45, null = True)
    referer = URLField("HTTP referer", null = True)
    query_string = TextField("Query string")
    query = TextField("The 'q' parameter in the query")

class MusicAccess(Model):
    user_agent = TextField("Client's user agent", null = True)
    ip_address = CharField("Client's IP address", max_length = 45, null = True)
    referer = URLField("HTTP referer", null = True)
    music_id = IntegerField("Id accessed")
