release: python manage.py migrate
web: gunicorn beatnik.wsgi
worker: python tasks/keep_alive.py
