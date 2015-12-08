from flask import Flask
from beacons.portal.views import portal

app = Flask(__name__)

app.register_blueprint(portal)
