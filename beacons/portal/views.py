from flask import Blueprint, render_template
import json
from flask.ext.session import Session
import flask
import httplib2

from apiclient import discovery
from oauth2client import client

portal = Blueprint('portal', __name__)
sess = Session()


@portal.route('/index')
@portal.route('/home')
def home():
    """
    Render Home Page
    """
    return render_template('index.jinja')


@portal.route('/')
def index():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v2', http_auth)
        files = drive_service.files().list().execute()
        return json.dumps(files)


@portal.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/drive.metadata.readonly',
        redirect_uri=flask.url_for('portal.oauth2callback', _external=True),
    )
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('portal.index'))
