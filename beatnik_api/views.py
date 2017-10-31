from beatnik_api import beatnik_api

@beatnik_api.route('/')
@beatnik_api.route('/index')

def index():
    return render_template("index.html")
