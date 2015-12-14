from flask import Blueprint, render_template, request
from flask.ext.session import Session
import flask
import requests
from oauth2client import client
import json
import config
from beacons import Beacon
from header import Header

portal = Blueprint('portal', __name__)
sess = Session()
session = requests.Session()


@portal.route('/')
def list_beacons():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        header = Header(credentials.access_token)
        auth_request = session.get(
            config.LIST_BEACONS, headers=header.__str__()
        )

        return render_template(
            'beacons.jinja', beacons=json.loads(auth_request.content)
        )


@portal.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope=config.SCOPE,
        redirect_uri=flask.url_for('portal.oauth2callback', _external=True),
    )

    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('portal.list_beacons'))


@portal.route('/register')
def register_beacons():
    return render_template('register.jinja')


@portal.route('/unregister')
def unregister_beacons():
    return render_template('unregister.jinja')


@portal.route('/registration-status', methods=['POST'])
def beacon_registration_status():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = Beacon(request.form.get('advid'))
        beacon.status = request.form.get('status')
        beacon.beacon_type = request.form.get('type')

        request_body = beacon.registration_request_body()
        header = Header(credentials.access_token)
        response = requests.post(
            config.REGISTER_BEACONS, data=json.dumps(request_body),
            headers=header.__str__()
        )

        return render_template(
            'registration_status.jinja', status=json.loads(response.content)
        )


@portal.route('/unregistration-status', methods=['POST'])
def beacon_unregistration_status():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon_name = request.form.get('name')
        header = Header(credentials.access_token)
        url = config.BEACON + beacon_name + config.DEACTIVATE
        response = requests.post(url, headers=header.__str__())
        status = \
            config.ERROR if response.status_code is 400 else config.SUCCESS

        return render_template('unregistration_status.jinja', status=status)
