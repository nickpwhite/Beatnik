from django.db.models import Model, CharField, TextField, URLField

class Request(Model):
    user_agent = TextField("Client's user agent", null = True)
    ip_address = CharField("Client's IP address", max_length = 45, null = True)
    referer = URLField("HTTP referer", null = True)
    query_string = TextField("Query string")
    query = TextField("The 'q' parameter in the query")
    path = TextField("The URL path", null = True)
