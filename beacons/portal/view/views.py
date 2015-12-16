from flask import Blueprint, render_template, request
import flask
import requests
from oauth2client import client
import json
from config import SUCCESS, ERROR, LIST_BEACONS, SCOPE, REGISTER_BEACONS
from beacons.portal.controller import controller

portal = Blueprint('portal', __name__)
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
        auth_request = session.get(LIST_BEACONS,
            headers=controller.get_header(credentials.access_token))

        return render_template(
            'beacons.jinja', beacons=json.loads(auth_request.content)
        )


@portal.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope=SCOPE,
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


@portal.route('/register', methods=['GET', 'POST'])
def register_beacons():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        if request.method == 'POST':
            beacon = controller.create_beacon(request.form)
            request_body = controller.registration_request_body(beacon)
            response = requests.post(
                REGISTER_BEACONS, data=json.dumps(request_body),
                headers=controller.get_header(credentials.access_token))
            return render_template('registration_status.jinja',
                status=json.loads(response.content)
            )

        return render_template('register.jinja')


@portal.route('/unregister', methods=['GET', 'POST'])
def unregister_beacons():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        if request.method == 'POST':
            beacon_details = controller.create_beacon_name(request.form)
            url = controller.get_deactivation_url(beacon_details)
            response = requests.post(
                url, headers=controller.get_header(credentials.access_token))
            status = ERROR if response.status_code is 400 else SUCCESS

            return render_template(
                'unregistration_status.jinja', status=status
            )

        return render_template('unregister.jinja')
