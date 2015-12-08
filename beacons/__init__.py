from flask import Flask

app = Flask(__name__)

from beacons.portal.views import portal
app.register_blueprint(portal)
