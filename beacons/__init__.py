from flask import Flask
from beacons.portal.view import portal, offer

app = Flask(__name__)

app.register_blueprint(portal)
app.register_blueprint(offer)
