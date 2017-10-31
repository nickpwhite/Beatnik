from flask import Flask

beatnik_api = Flask(__name__)

from beatnik_api import views
