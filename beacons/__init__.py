from flask import Flask
from beacons.portal.view import portal

app = Flask(__name__)

app.register_blueprint(portal)
